from typing import Any, Union
from google.cloud import storage
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.logger import ILogger


class CloudStorage(IStorage):
    _bucket: storage.Bucket
    _bucket_name: str

    def __init__(self, connection: storage.Client, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger
        self._bucket_name = ""

    @property
    def bucket(self) -> Any:
        if not self._bucket:
            raise ResourceNameNotFound("Storage not found, please provide a name to it")
        return self._bucket

    @bucket.setter
    def bucket(self, name: str):
        self._bucket = self.connection.bucket(name)

    def save_file(
        self,
        data: str,
        file_path: str,
        content_type: str,
        is_public: bool = False,
    ) -> bool:
        self.logger.info(
            f"Saving a file with content-type as '{content_type}' in '{file_path}'"
        )
        try:
            blob = self._bucket.blob(file_path)
            blob.upload_from_string(data=data, content_type=content_type)
            if is_public:
                blob.make_public()
        except Exception as err:  # pylint: disable=W0718
            self.logger.error(
                f"An error occurred when try to save a file in Cloud Storage. Error detail: {err}"
            )
            return False
        return True

    def get_file(self, file_path: str) -> Union[bytes, None]:
        try:
            blob = self._bucket.blob(file_path)
            return blob.download_as_bytes()
        except Exception as err:  # pylint: disable=W0612,W0718
            self.logger.error(
                f"An error occurred when try to get a file in CloudStorage. Error detail: {err}"
            )
            return None

    def ls(self, path: str) -> list[str]:
        return list(self._bucket.list_blobs(prefix=path))

    def delete(self, file_path: str) -> bool:
        try:
            blob = self._bucket.blob(file_path)
            generation_match_precondition = None
            blob.reload()
            generation_match_precondition = blob.generation
            blob.delete(if_generation_match=generation_match_precondition)
        except Exception as err:  # pylint: disable=W0612,W0718
            return False
        return True
