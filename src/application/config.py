from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(".env")

class Settings(BaseSettings):
    OPENWEATHER_API_KEY: str
    OPENWEATHER_BASE_URL: str

    AWS_REGION: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: str
    MINIO_ENDPOINT: str
    DYNAMODB_ENDPOINT: str
    DYNAMODB_TABLE: str
    BUCKET_NAME: str

    OBJECT_EXPIRY_MINUTES: int

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()

dynamodb_table_config = {
        "TableName": "YourTableName",
        "KeySchema": [
            {"AttributeName": "PartitionKey", "KeyType": "HASH"},
            # {"AttributeName": "SortKey", "KeyType": "RANGE"}
        ],
        "AttributeDefinitions": [
            {"AttributeName": "PartitionKey", "AttributeType": "S"},
            # {"AttributeName": "SortKey", "AttributeType": "N"}
        ],
        "ProvisionedThroughput": {
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    }