import boto3
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.storage import IStorage
from cloud_components.common.interface.libs.enviroment import IEnviroment
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.cloud.aws.repository.s3 import S3


class StorageFactory(IFactory[IStorage]):
    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        self.logger = logger
        self.env = env

    def manufacture(self) -> IStorage:
        connection = boto3.resource(
            "s3",
            aws_access_key_id=self.env.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=self.env.get("AWS_SECRET_ACCESS_KEY"),
            endpoint_url=self.env.get("AWS_ENDPOINT_URL"),
        )
        return S3(connection=connection, logger=self.logger)
