from abc import ABC, abstractmethod

from cloud_components.common.interface.cloud.event import IEvent
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.cloud.storage import IStorage


class ICloudFacade(ABC):

    @abstractmethod
    def event(self) -> IEvent:
        pass

    @abstractmethod
    def function(self) -> IFunction:
        pass

    @abstractmethod
    def queue(self) -> IQueue:
        pass

    @abstractmethod
    def storage(self) -> IStorage:
        pass
