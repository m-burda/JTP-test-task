from botocore.exceptions import ClientError

from application.config import DYNAMODB_TABLE_CONFIG, settings
from application.dependencies import get_session


async def setup_storage():
    session = get_session()
    try:
        async with session.client(
            "dynamodb", endpoint_url=settings.DYNAMODB_ENDPOINT
        ) as dynamodb:
            await dynamodb.create_table(**DYNAMODB_TABLE_CONFIG)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceInUseException":
            pass
        else:
            raise e
