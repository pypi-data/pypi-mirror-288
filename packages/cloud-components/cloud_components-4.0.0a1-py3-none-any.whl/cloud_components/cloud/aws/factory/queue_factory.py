import boto3

from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.queue import IQueue
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.cloud.aws.repository.sqs import Sqs


class QueueFactory(IFactory[IQueue]):
    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        self.logger = logger
        self.env = env

    def manufacture(self) -> IQueue:
        connection = boto3.resource(
            "sqs",
            aws_access_key_id=self.env.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=self.env.get("AWS_SECRET_ACCESS_KEY"),
            endpoint_url=self.env.get("AWS_ENDPOINT_URL"),
        )
        return Sqs(connection=connection, logger=self.logger)
