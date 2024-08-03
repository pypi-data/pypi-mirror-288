from typing import Any, Union
from cloud_components.common.errors.invalid_resource import ResourceNameNotFound
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.libs.logger import ILogger


class Lambda(IFunction):
    _name: Union[str, None] = None

    def __init__(self, connection: Any, logger: ILogger) -> None:
        self.connection = connection
        self.logger = logger

    @property
    def function(self):
        if not self._name:
            raise ResourceNameNotFound(
                "Function not found, please provide a name to it"
            )
        return self._name

    @function.setter
    def function(self, value: str):
        self._name = value

    def execute(self, payload: bytes):
        raise NotImplementedError
