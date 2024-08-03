from typing import cast
from cloud_components.common.interface.libs.logger import ILogger

try:
    from loguru import logger
except ImportError:
    pass


class Loguru:
    def load(self) -> ILogger:
        return cast(ILogger, logger)
