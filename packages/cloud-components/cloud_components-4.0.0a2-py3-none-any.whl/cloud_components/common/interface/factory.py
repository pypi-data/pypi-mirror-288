from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")


class IFactory(ABC, Generic[T]):
    @abstractmethod
    def manufacture(self) -> T:
        pass
