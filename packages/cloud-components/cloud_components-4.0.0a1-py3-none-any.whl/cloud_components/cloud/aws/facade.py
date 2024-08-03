from cloud_components.common.interface.facade import ICloudFacade
from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.aws.factory.event_factory import Eventfactory
from cloud_components.cloud.aws.factory.function_factory import FunctionFactory
from cloud_components.cloud.aws.factory.queue_factory import QueueFactory
from cloud_components.cloud.aws.factory.storage_factory import StorageFactory


class AWSFacade(ICloudFacade):
    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        self.logger = logger
        self.env = env

    def event(self) -> IEvent:
        return Eventfactory(self.logger, self.env).manufacture()

    def function(self) -> IFunction:
        return FunctionFactory(self.logger, self.env).manufacture()

    def queue(self) -> IQueue:
        return QueueFactory(self.logger, self.env).manufacture()

    def storage(self) -> IStorage:
        return StorageFactory(self.logger, self.env).manufacture()
