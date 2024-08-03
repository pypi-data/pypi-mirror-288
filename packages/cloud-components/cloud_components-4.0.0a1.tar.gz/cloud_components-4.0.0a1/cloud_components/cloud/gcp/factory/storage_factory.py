from google.cloud import storage
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.repository.cloud_storage import CloudStorage


class StorageFactory(IFactory[IStorage]):
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def manufacture(self) -> IStorage:
        return CloudStorage(connection=storage.Client(), logger=self.logger)
