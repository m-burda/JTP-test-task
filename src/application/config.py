from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env")


class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    OPENWEATHER_BASE_URL: str

    AWS_DEFAULT_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    BUCKET_NAME: str
    MINIO_ENDPOINT: str
    DYNAMODB_ENDPOINT: str
    DYNAMODB_TABLE_NAME: str

    OBJECT_EXPIRY_MINUTES: int

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()

DYNAMODB_TABLE_CONFIG = {
    "TableName": settings.DYNAMODB_TABLE_NAME,
    "KeySchema": [
        {"AttributeName": "id", "KeyType": "HASH"},
        # {"AttributeName": "SortKey", "KeyType": "RANGE"}
    ],
    "AttributeDefinitions": [
        {"AttributeName": "id", "AttributeType": "S"},
    ],
    "ProvisionedThroughput": {"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
}
