###############################################################################
##  ViQi BisQue                                                              ##
##  ViQi Inc                                                                 ##
## ------------------------------------------------------------------------- ##
##                                                                           ##
##     Copyright (c) 2007-2023                                               ##
##     by the ViQI Inc                                                       ##
##                            All rights reserved                            ##
##                                                                           ##
## Redistribution and use in source and binary forms, with or without        ##
## modification, are permitted provided that the following conditions are    ##
## met:                                                                      ##
##                                                                           ##
##     1. Redistributions of source code must retain the above copyright     ##
##        notice, this list of conditions, and the following disclaimer.     ##
##                                                                           ##
##     2. Redistributions in binary form must reproduce the above copyright  ##
##        notice, this list of conditions, and the following disclaimer in   ##
##        the documentation and/or other materials provided with the         ##
##        distribution.                                                      ##
##                                                                           ##
##                                                                           ##
## THIS SOFTWARE IS PROVIDED BY <COPYRIGHT HOLDER> ''AS IS'' AND ANY         ##
## EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE         ##
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR        ##
## PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> OR           ##
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,     ##
## EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,       ##
## PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR        ##
## PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF    ##
## LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING      ##
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS        ##
## SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.              ##
##                                                                           ##
## The views and conclusions contained in the software and documentation     ##
## are those of the authors and should not be interpreted as representing    ##
## official policies, either expressed or implied, of <copyright holder>.    ##
###############################################################################

import concurrent.futures
import fnmatch
import logging
import os
import posixpath
import random
import string
import threading
import time
from queue import Queue
from typing import BinaryIO, Callable, Dict, Optional
from urllib.parse import quote as urlquote

import boto3
import botocore

# import pytz
import tenacity
from botocore.credentials import RefreshableCredentials
from botocore.session import get_session
from bq.metadoc.formats import Metadoc
from requests_toolbelt import MultipartEncoder

from vqapi.exception import BQApiError, code_to_exception
from vqapi.util import normalize_unicode

from .base_proxy import FuturizedServiceProxy

log = logging.getLogger("vqapi.services")

# End token for loading files to be transferred
_FILES_LOADED = object()


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


class ImportProxy(FuturizedServiceProxy):
    service_name = "import"
    upload_prefix = "/home/uploads"  # TODO fetch from user prefences
    upload_default_mount = "/home"  # TODO fetch from user

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.protocol_info_map = {"/home": None}  # Map of store to best protocol

    @classmethod
    def destination_path(cls, srcpath, dstpath):
        """Create a valid destination path from src and dst

        Examples:
          Source known, destination None
          destination_path("filename.tif", None) -> upload_prefix/filename.tif
          destination_path("path2/to/file/filename.tif", None) -> upload_prefix/path/to/file/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", None) -> upload_pefix/filename.tif

          Source None, destination
          destination_path(None, "filename.tif") -> upload_mount/filename.tif
          destination_path(None, "relatitive_path/filename.tif") -> upload_mount/relative_path/filename.tif
          destination_path(None, "/home/project/to/path/filename.tif") -> "/home/project/to/path/filename.tif"

          Source and Destination -> use dest
          destination_path("filename.tif", "filename.tif") -> upload_mount/filename.tif
          destination_path("path2/to/file/filename.tif", "filename.tif") -> $upload_mount/filename.tif
          destination_path("path2/to/file/filename.tif", "relative_path/filename.tif") -> $upload_mount/relatice_path/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", "/home/poject/path2/filename.tif") -> /home/project/path2/filename.tif

          Source and Destination Dir (marked by trailing "/" -> use src + dest
          destination_path("filename.tif", "apath/") -> $upload_mount/apath/filename.tif
          destination_path("path2/to/file/filename.tif", "apath/") -> $upload_mount/apath/filename.tif
          destination_path("/home/user/path2/to/file/filename.tif", "/home/mount/apath/") -> /home/mount/apath/filename.tif

        """
        if dstpath is None:
            dstpath = cls.upload_prefix
            if srcpath[0] == "/":
                # srcpath is fullpath.. we cannot really guess how much of path to copy so just use name
                return posixpath.join(dstpath, os.path.basename(srcpath))
            # join relative path to default_prefix
            return posixpath.join(dstpath, srcpath)

        if dstpath[-1] == "/":  # DIR destination
            dstpath = posixpath.join(dstpath, os.path.basename(srcpath))

        if dstpath[0] != "/":  # NOT absolute upload, join with def
            dstpath = posixpath.join(cls.upload_default_mount, dstpath)

        return dstpath

    # @functools.lru_cache(maxsize=None)
    def transfer_protocol_info(self, dirpath: str = None, protocol: str = None) -> Optional[Metadoc]:
        """Return proto info for best transfer_protocol

        Args:
            dirpath : the destination directory storepath
        Returns:
           A proto_info dict: with protocol specific information
        """
        if dirpath is None:
            dirpath = self.upload_prefix
        if dirpath[0] == "/":
            dirpath = dirpath[1:]

        # protocol dependes on directory of path.. strip filename
        # path = os.path.dirname(path)
        mount, dirpath = dirpath.split("/", 1)  # 'home/hello/aaa.jpg' -> ['home', 'hello', 'aaa.jpg']
        if (mount, protocol, dirpath) in self.protocol_info_map:
            # log.info("CACHED %s", dirpath)
            return self.protocol_info_map[(mount, protocol, dirpath)]

        if protocol is not None:
            available_protocols = [Metadoc.create_doc("protocol", type=protocol)]
        else:
            url = posixpath.join("/transfer_protocol", mount, urlquote(dirpath))
            log.debug("protocol check %s", url)
            protocols = self.fetch(url)
            # Choose the preferred one by order
            code_to_exception(protocols)
            proto_doc = protocols.doc()
            # log.info("PROTO %s", str(proto_doc))
            available_protocols = proto_doc.path_query("protocol")

        for proto in available_protocols:
            # check if we know one
            if hasattr(self, "transfer_" + proto.attrib["type"]):
                # we know how to transfer, grab info
                proto_info = self.fetch(
                    posixpath.join("/transfer_protocol", mount, urlquote(dirpath)),
                    params={"protocol": proto.attrib["type"]},
                )
                code_to_exception(proto_info)
                proto_info = proto_info.doc()
                self.protocol_info_map[(mount, None, dirpath)] = proto_info
                self.protocol_info_map[(mount, proto, dirpath)] = proto_info
                return proto_info
        return None

    def transfer_batch(
        self,
        srcs: str | list,
        dstdir: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
        register: bool = True,
    ):
        """Transfer a batch of files and directories  in parallel to a destinatation

        Args
        """
        log.debug("transfer_batch %s", srcs)
        file_queue = Queue()
        futuremap = {}
        localvar = threading.local()
        localvar.session = self.session

        if isinstance(srcs, str) or not hasattr(srcs, "__iter__"):
            srcs = [srcs]

        with concurrent.futures.ThreadPoolExecutor(
            max_workers=os.cpu_count(),
            initializer=thread_session_initialize,
            initargs=(localvar, self.session, protocol),
        ) as executor:
            # Load the file_queue in a task in case  this is large tree
            futuremap = {
                executor.submit(initiate_batch_transfer, srcs=srcs, file_queue=file_queue, dstdir=dstdir): _FILES_LOADED
            }
            transferred, failed = self.parallel_transfer(localvar, executor, futuremap, file_queue)
        log.debug("batch transferred:%s  failed:%s", transferred, failed)

        # current handled by s3_transfer itself.
        # if transferred:
        #    dirs = self.session.service("dirs")
        #    dirs.refresh(os.path.commonpath(srcs))

        return transferred, failed

    def parallel_transfer(self, localvar, executor, futuremap, file_queue):
        """process the tranfer queue using the parallel threads EXECUTER
        Args:
           localvar.session : threadlocal variable for accessing session
           executer:  A ThreadPoolManager
           futuremap:  dict[future]->filepath
           filequeue:  thread queue of futures to process
        """
        transferred = []
        failed = []
        # Futuremap is a dict thread fture-> (filepath| LOADED_TOKEN)
        # Should arrive here with a task filling the file_queue
        while futuremap:
            # Wait for/force a task to finish, but bail after 1 sec so we check the file_queue
            done, not_done = concurrent.futures.wait(
                futuremap, timeout=1, return_when=concurrent.futures.FIRST_COMPLETED
            )
            # process any completed futures
            for future in done:
                try:
                    file_path = futuremap.pop(future)
                    future_res = future.result()
                    if file_path == _FILES_LOADED:
                        log.info("loaded %s files for transfer", future_res)
                        continue
                    transferred.append(file_path)
                except (TimeoutError, concurrent.futures.CancelledError):
                    failed.append((file_path, "timeout or cancelleed"))
                except Exception as exc:
                    log.exception("%s generated an exception: %s", file_path, exc)
                    failed.append((file_path, exc))

            # Grab any files waiting to be uploaded and add them as tasks
            while not file_queue.empty():
                file_tuple = file_queue.get()
                futuremap[executor.submit(thread_upload, localvar, file_tuple)] = file_tuple[1]

        return transferred, failed

    def transfer_file(
        self,
        srcpath: str,
        dstpath: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
        register: bool = True,
    ):
        """Transfer a file to the system
        Args:
          srcpath : the path to the local file or filename to give to the file object
          xml     :
        """
        with open(srcpath, "rb") as src:
            return self.transfer_fileobj(
                src, xml=xml, callback=callback, srcpath=srcpath, dstpath=dstpath, protocol=protocol, register=register
            )

    def transfer_fileobj(
        self,
        fileobj: BinaryIO,
        srcpath: str = None,
        dstpath: str = None,
        xml: Metadoc = None,
        callback: Callable = None,
        protocol: str = None,
        register: bool = True,
    ):
        if srcpath is None and hasattr(fileobj, "name"):
            srcpath = fileobj.name
        dstpath = self.destination_path(srcpath, dstpath)
        log.info("transfer %s -> %s", srcpath, dstpath)
        transfer_info = self.transfer_protocol_info(dirpath=os.path.dirname(dstpath), protocol=protocol)
        # log.info("TRANS %s", str(transfer_info))
        # Use the protocol to  find a method to transfer the file
        if transfer_info is not None:
            protocol = transfer_info.path_query("protocol")[0]
            transfer_fct = getattr(self, "transfer_" + protocol.attrib["type"])
            if transfer_fct is not None:
                return transfer_fct(
                    fileobj=fileobj,
                    dstpath=dstpath,
                    xml=xml,
                    callback=callback,
                    transfer_info=transfer_info,
                    register=register,
                )
        raise BQApiError("No transfer protocol supported for file transfer")

    def transfer_multipart(
        self, fileobj: BinaryIO, dstpath: str, xml=None, callback=None, transfer_info=None, register=True
    ):
        log.info("transfer_multpart %s -> %s", fileobj.name, dstpath)
        fields = {}
        filename = normalize_unicode(fileobj.name)
        fields["file"] = (
            os.path.basename(filename),
            fileobj,
            "application/octet-stream",
        )
        if xml is not None:
            fields["file_resource"] = (None, xml, "application/xml")
        if fields:
            # https://github.com/requests/toolbelt/issues/75
            m = MultipartEncoder(fields=fields)
            m._read = m.read  # pylint: disable=protected-access
            # filesize = os.fstat (fileobj).st_size
            # haveread = 0

            def reader(size):
                buff = m._read(8192 * 1024)  # 8MB
                # haveread += 8192
                if callable(callback):
                    callback(len(buff))
                return buff

            m.read = reader
            # ID generator is used to force load balancing operations
            response = self.post(
                "transfer_" + id_generator(),
                data=m,
                headers={"Accept": "text/xml", "Content-Type": m.content_type},
            )
            code_to_exception(response)
            return response.doc()

    def transfer_binary(self, fileobj, dstpath, xml=None, callback=None, transfer_info=None, register=True):
        log.info("transfer_binary %s -> %s", fileobj.name, dstpath)
        response = self.post(
            posixpath.join("transfer_direct", urlquote(dstpath[1:])),
            data=fileobj,
            headers={"Content-Type": "application/octet-stream"},
        )
        code_to_exception(response)

        if xml is None:
            return None

        if register and xml is not None:
            blobs = self.session.service("blobs")
            blob = blobs.register(path=dstpath[1:], resource=xml)

        # blob = blobs.register(posixpath.join(path, filename))
        # if xml:
        #     meta = self.session.service('meta')
        #     # Find the uploaded blob and register with XML
        #     for kid in Metadoc.from_tagxml(xml):
        #         blob.append(kid)
        #     meta.put(blob.get("resource_uniq"), data=blob)
        return blob

    def transfer_s3(
        self,
        fileobj: BinaryIO,
        dstpath,
        xml=None,
        callback=None,
        transfer_info=None,
        register=True,
        **kw,
    ):
        """Transfer a file to s3
        Args :
            fileob  : the options open file object
            dstpath : a store path i.e. /storename/d1/d2
            xml     : xml to registered
            info    : metadoc
                       <transfer>
                         <protocol type="fsxlustre">
                         <info>
                           <Credentials>
                            <AccessKeyId></AccessKeyId>
                            <SessionToken></SessionToken>
                            <SecretAccessKey>TMWnEWRxPak+Pebk8ngp28fp5tvoVlg3yrbxfQ5x</SecretAccessKey>
                            <Expiration>2022-06-28 19:32:58+00:00</Expiration>
                           </Credentials>
                           <Destination>
                             <S3>
                              <Region>us-west-2</Region>
                              <Bucket>viqi-lustre-staging</Bucket>
                              <Folder>users/admin/testdir</Folder>
                              <Uid>1000</Uid>
                              <Gid>1000</Gid>
                            </S3>
                          </Destination>
                     </protocol>
                   </transfer>
        Returns:
         the list of files transferred
        """
        # Get cliend creds from info
        log.info("transfer_s3 %s -> %s", fileobj.name, dstpath)

        filename = os.path.basename(dstpath)
        # partial_path = "/".join(dstpath.split("/")[2:-1])
        partial_path = ""
        try:
            upload_ok = False
            s3client = None
            for _ in range(3):  # Attempt upload 3 times with expired token handling
                info = transfer_info.path_query("//info")[0].to_json()
                s3_info = info["info"]
                log.debug(
                    "S3 INFO %s destpath:%s filename:%s fileobj:%s",
                    s3_info,
                    dstpath,
                    filename,
                    fileobj,
                )
                if s3client is None:
                    s3client = self._s3_client(s3_info, transfer_info)

                try:
                    if not self._s3_dir_exists(s3client, s3_info, partial_path):
                        self._s3_create_dirs(s3client, s3_info, partial_path)
                    s3client.upload_fileobj(
                        fileobj,
                        Bucket=s3_info["Destination"]["S3"]["Bucket"],
                        Key=posixpath.join(
                            s3_info["Destination"]["S3"]["Folder"],
                            partial_path,
                            filename,
                        ),
                        Callback=self._s3_progress(fileobj, callback=callback),
                        ExtraArgs={
                            "Metadata": {
                                "user-agent": "aws-fsx-lustre",
                                "file-permissions": "0100660",
                                "file-owner": s3_info["Destination"]["S3"]["Uid"],
                                "file-group": s3_info["Destination"]["S3"]["Gid"],
                            }
                        },
                    )
                    fileobj.close()
                    upload_ok = True
                    break
                except botocore.exceptions.ClientError as error:
                    code = error.response["Error"]["Code"]
                    log.warn("AWS Client error %s -> code %s", error, code)
                    if code in ("ExpiredToken", "AccessDenied"):
                        transfer_info = self._s3_refresh(transfer_info)
                        s3client = None
                        fileobj = open(fileobj.name, "rb")  # Potential File Obj Leak
                        continue

            if not upload_ok:
                raise BQApiError(f"Failed upload of {filename}. S3 token invalid")

            dirs = self.session.service("dirs")
            # print("REFRESHING in 10")
            # time.sleep(10)
            dirs.refresh(dstpath)

            if xml is None or not register:
                return None

            # register the uploaded file with xml if available
            # dirs = self.session.service("dirs")
            blobs = self.session.service("blobs")
            if isinstance(xml, str):
                xml = Metadoc.from_naturalxml(xml)

            try:
                # time.sleep(2)
                # dirs.list_files(dstpath)  # KGK: List needed to force s3 transfer pathdb (review server side)
                for attempt in tenacity.Retrying(stop=tenacity.stop_after_attempt(3), wait=tenacity.wait_fixed(2)):
                    blobdoc = blobs.register(path=dstpath, resource=xml)
                    return blobdoc
            except tenacity.RetryError:
                log.error("Regsitration failed after upload")

        except boto3.exceptions.S3UploadFailedError:
            log.exception("During upload of %s", filename)
        return None

    def _s3_create_dirs(self, s3client, s3_info: dict, path: str):
        """Ensure directory exists and has proper metadata (permissions)"""
        head, tail = posixpath.split(path)
        if not tail:  # special case for trailing '/'
            head, tail = posixpath.split(head)
        if head and tail:
            # check if head exists
            if not self._s3_dir_exists(s3client, s3_info, head):
                # log.debug("recurse %s", head)
                self._s3_create_dirs(s3client, s3_info, head)
        #
        self._s3_mkdir(s3client, s3_info, path)

    def _s3_dir_exists(self, s3client, s3_info, dirpath):
        """Check if user rooted directory exists"""
        try:
            # log.debug("s3_direxists %s", dirpath)
            s3client.head_object(
                Bucket=s3_info["Destination"]["S3"]["Bucket"],
                Key=posixpath.join(s3_info["Destination"]["S3"]["Folder"], dirpath, ""),
            )
            return True
        except botocore.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            log.debug("s3direxists error %s", code)
        return False

    def _s3_mkdir(self, s3client, s3_info, dirpath):
        try:
            # log.debug("s3_mkdir %s ", dirpath)
            s3client.put_object(
                Bucket=s3_info["Destination"]["S3"]["Bucket"],
                Key=posixpath.join(s3_info["Destination"]["S3"]["Folder"], dirpath, ""),
                Metadata={
                    "file-owner": s3_info["Destination"]["S3"]["Uid"],
                    "file-group": s3_info["Destination"]["S3"]["Gid"],
                },
            )
        except botocore.exceptions.ClientError as error:
            code = error.response["Error"]["Code"]
            log.debug("ended on %s", code)

    def _s3_client(self, s3_info, transfer_info: Dict):
        """Create a long-lasting s3 Session suitable for caching
        Args:
           s3_info : {"AccessKeyId": "ID",
                       "SessionToken": "Token", "SecretAccessKey":
                       "Secret", "Expiration": "Expires"}

        Returns:
          a S3 boto client
        TODO :  Utilize a refreshable credential provider
                https://stackoverflow.com/questions/61899028/where-can-i-find-the-documentation-for-writing-custom-aws-credential-provider-us
        """
        log.debug("s3 session create client")
        # session = boto3.session.Session()  # see https://github.com/boto/boto3/issues/801
        session = RefreshableBotoSession(self, s3_info, transfer_info).refreshable_session()
        s3client = session.client("s3")
        return s3client

        raise BQApiError("transfer_s3 not implemented")

    def _s3_refresh(self, transfer_info: Metadoc) -> Metadoc:
        """Fetch new credential when expired
            info    : metadoc
                       <transfer>
                         <protocol type="fsxlustre">
                         <info>
                           <Credentials>
                            <AccessKeyId></AccessKeyId>
                            <SessionToken></SessionToken>
                            <SecretAccessKey>TMWnEWRxPak+Pebk8ngp28fp5tvoVlg3yrbxfQ5x</SecretAccessKey>
                            <Expiration>2022-06-28 19:32:58+00:00</Expiration>
                           </Credentials>
                           <Destination>
                             <S3>
                              <Region>us-west-2</Region>
                              <Bucket>viqi-lustre-staging</Bucket>
                              <Folder>users/admin/testdir</Folder>
                            </3>
                          </Destination>
                     </protocol>
                   </transfer>
        Returns:
         the list of files transferred
        """
        info = self.post("/transfer_protocol", data=transfer_info)
        code_to_exception(info)
        info = info.doc()
        log.info("s3_session refresh %s", info.to_json())
        return info

    def _s3_progress(self, fileobj, callback):
        return S3Progress(fileobj, callback=callback)

    def transfer_fsxlustre(self, *args, **kw) -> Metadoc:
        return self.transfer_s3(*args, **kw)

    def ingester_list(self) -> Metadoc:
        """List available scripts"""
        scripts = self.fetch("ingest")
        code_to_exception(scripts)
        return scripts.doc()

    def ingester_run(self, script_name, storepath, preview=True, **processor_args) -> Metadoc:
        """Run a registration script"""
        run = Metadoc(tag="resource")
        run.add_tag("processor", value=script_name)
        run.add_tag("path", value=storepath)
        if processor_args:
            for k, v in processor_args.items():
                run.add_tag(k, value=v)
        resp = self.post("ingest", data=run, params={"preview": preview})
        code_to_exception(resp)
        return resp.doc()


class S3Progress:
    def __init__(self, fileobj, size=None, callback=None):
        self._filename = fileobj.name
        self._size = float(size or os.fstat(fileobj.fileno()).st_size)
        self._transferred = 0
        self._lock = threading.Lock()
        self.callback = callback
        self._progress_min_period = 10
        self._progress_last_time = 0

    def __call__(self, transferred):
        with self._lock:
            self._transferred += transferred
            # minimum period for updates
            if time.time() - self._progress_last_time > self._progress_min_period or self._transferred == self._size:
                value = (self._transferred / self._size) * 100
                log.info("S3 transfer %s %s/%s (%.2f%%)", self._filename, self._transferred, int(self._size), value)
                self._progress_last_time = time.time()

        if self.callback:
            self.callback(transferred)


class RefreshableBotoSession:
    """
    Boto Helper class which lets us create a refreshable session so that we can cache the client or resource.

    Usage
    -----
    session = RefreshableBotoSession().refreshable_session()

    client = session.client("s3") # we now can cache this client object without worrying about expiring credentials
    """

    def __init__(self, service, s3_info, transfer_info):
        """
        aws_creds { AccessKeyId, SecretAccessKey, SessionToken, Expiration, }
        """

        self.import_service = service
        self.creds = s3_info["Credentials"]
        self.info = transfer_info

        # self.aws_access_key_id  = creds["AccessKeyId"]
        ##self.aws_secret_access_key  = creds["SecretAccessKey"]
        # self.aws_session_token  = creds["SessionToken"]

    def __get_session_credentials(self):
        """
        Get session credentials
        """
        if self.creds:
            credentials = {
                "access_key": self.creds.get("AccessKeyId"),
                "secret_key": self.creds.get("SecretAccessKey"),
                "token": self.creds.get("SessionToken"),
                "expiry_time": self.creds.get("Expiration"),
            }
            self.creds = None
            log.debug("original credentals %s", credentials)
            return credentials

        info = self.import_service._s3_refresh(self.info)
        creds = info.path_query("//info")[0].to_json()["info"]["Credentials"]
        credentials = {
            "access_key": creds.get("AccessKeyId"),
            "secret_key": creds.get("SecretAccessKey"),
            "token": creds.get("SessionToken"),
            "expiry_time": creds.get("Expiration"),
        }

        # session_credentials = session.get_credentials().get_frozen_credentials()
        # credentials = {
        #     "access_key": session_credentials.access_key,
        #     "secret_key": session_credentials.secret_key,
        #     "token": session_credentials.token,
        #     "expiry_time": datetime.fromtimestamp(time() + self.session_ttl).replace(tzinfo=pytz.utc).isoformat(),
        # }
        log.debug("refresh credentals %s", credentials)

        return credentials

    def refreshable_session(self) -> boto3.session.Session:
        """
        Get refreshable boto3 session.
        """
        # Get refreshable credentials
        refreshable_credentials = RefreshableCredentials.create_from_metadata(
            metadata=self.__get_session_credentials(),
            refresh_using=self.__get_session_credentials,
            method="sts-assume-role",
        )

        # attach refreshable credentials current session
        session = get_session()
        session._credentials = refreshable_credentials
        # session.set_config_variable("region", self.region_name)
        autorefresh_session = boto3.session.Session(botocore_session=session)

        return autorefresh_session


def initiate_batch_transfer(
    srcs: list,
    file_queue: Queue,
    dstdir: str | None = None,
    includes: list[str] | None = None,
    excludes: list[str] | None = None,
):
    """Transfer a list of files
    Args:
      srcs: a single str or list of directories/files to transfer
      file_queue: a thread queue to add entries
      includes: a list of glob expressions to include in transfer
      excludes: a list of glob expressions to exclude from transfer

    Returns:
      The number of files added to the queue

    """

    file_count = 0

    def add_files(files, root):
        nonlocal file_count  # get file_count from outside scope
        root = os.path.join(root, "")
        for f1 in files:
            if includes and not any(fnmatch.fnmatch(f1, include) for include in includes):
                log.info("Skipping %s: not included", f1)
                continue
            if excludes and any(fnmatch.fnmatch(f1, exclude) for exclude in excludes):
                log.info("Skipping %s: excluded", f1)
                continue
            log.debug("appending %s with root %s", f1, root)
            # metatable.append(f1, root)
            # Add full localpath and partial destination path
            file_queue.put((f1, f1[len(root) :], dstdir))
            file_count += 1

    for srctree in srcs:
        if os.path.isdir(srctree):
            directory = os.path.abspath(srctree).replace("\\", "/")
            parent = os.path.dirname(directory).replace("\\", "/")
            for root, _, files in os.walk(directory):
                add_files((os.path.join(root, f1).replace("\\", "/") for f1 in files), root=parent)
        elif os.path.isfile(srctree):
            parent = os.path.dirname(srctree).replace("\\", "/")
            add_files([srctree.replace("\\", "/")], root=parent)

    return file_count


def thread_session_initialize(localvar, session, protocol):
    """Create a cloned session
    and import service for use by threaded_upload
    This is called once for each thread created by ThreadPool
    """
    localvar.session = session.copy()
    localvar.import_svc = session.service("import")
    localvar.protocol = protocol


def thread_upload(localvar, file_tuple: tuple[str, str]):
    """Upload a single file
    Args:
       localvar is a threadlocal object containing session, and imp_svc (import_service instance)

    """
    imp_svc = localvar.import_svc
    protocol = localvar.protocol
    # register = lovalvar.register

    full_path = file_tuple[0]
    path = file_tuple[1]
    dstdir = file_tuple[2]

    if dstdir:
        path = posixpath.join(dstdir, path)

    log.info("thread_upload of %s", path)
    # xml
    imp_svc.transfer_file(srcpath=full_path, dstpath=path, protocol=protocol)
