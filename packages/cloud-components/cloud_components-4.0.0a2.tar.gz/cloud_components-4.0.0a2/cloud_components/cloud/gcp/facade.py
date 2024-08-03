from cloud_components.common.interface.facade import ICloudFacade
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.gcp.factory.storage_factory import StorageFactory


class GCSFacade(ICloudFacade):
    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        self.logger = logger
        self.env = env

    def event(self) -> IEvent:
        raise NotImplementedError

    def function(self) -> IFunction:
        raise NotImplementedError

    def queue(self) -> IQueue:
        raise NotImplementedError

    def storage(self) -> IStorage:
        return StorageFactory(logger=self.logger).manufacture()
