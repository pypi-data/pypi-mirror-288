import boto3

from cloud_components.cloud.aws.repository.lambda_function import Lambda
from cloud_components.common.interface.factory import IFactory
from cloud_components.common.interface.cloud.function import IFunction
from cloud_components.common.interface.libs.logger import ILogger
from cloud_components.common.interface.libs.enviroment import IEnviroment


class FunctionFactory(IFactory[IFunction]):
    def __init__(self, logger: ILogger, env: IEnviroment) -> None:
        self.logger = logger
        self.env = env

    def manufacture(self) -> IFunction:
        connection = boto3.client(
            "lambda",
            aws_access_key_id=self.env.get("AWS_ACCESS_KEY"),
            aws_secret_access_key=self.env.get("AWS_SECRET_ACCESS_KEY"),
            endpoint_url=self.env.get("AWS_ENDPOINT_URL"),
        )
        return Lambda(connection=connection, logger=self.logger)
