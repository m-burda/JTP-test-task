from aiohttp import ClientError

from application.config import settings, dynamodb_table_config
from application.dependencies import get_session


async def setup_storage():
    session = get_session()
    try:
        async with session.client('s3', endpoint_url=settings.MINIO_ENDPOINT) as s3:
            await s3.create_bucket(Bucket=settings.BUCKET_NAME)
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            pass
        else:
            raise e

    try:
        async with session.client("dynamodb", endpoint_url=settings.DYNAMODB_ENDPOINT) as dynamodb:
            await dynamodb.create_table(TableName=settings.DYNAMODB_TABLE,
                                        KeySchema=dynamodb_table_config["KeySchema"],
                                        AttributeDefinitions=dynamodb_table_config["AttributeDefinitions"],
                                        ProvisionedThroughput=dynamodb_table_config["ProvisionedThroughput"]
                                        )
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            pass
        else:
            raise e