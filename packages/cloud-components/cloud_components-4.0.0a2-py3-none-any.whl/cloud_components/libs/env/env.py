import os
from typing import Any, Callable, Union

from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.common.interface.libs.logger import ILogger

try:
    from dotenv import load_dotenv
except ImportError as err:
    pass


class Dotenv(IEnviroment):  # pylint: disable=C0115
    def __init__(self, logger: ILogger) -> None:
        self.logger = logger

    def load(self):
        self.logger.info("Loading enviroment variables")
        load_dotenv()

    def get(
        self,
        env_name: str,
        cast: Union[Callable[[Any], Any], None] = None,
        defalt: Union[Any, None] = None,
    ) -> Any:
        value = os.getenv(env_name, defalt)
        return value if not cast else cast(value)
