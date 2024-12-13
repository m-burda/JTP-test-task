import aioboto3
from fastapi import Depends

from application.config import settings
from services.weather_service import WeatherService


def get_session() -> aioboto3.Session:
    return aioboto3.Session(
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )


async def get_s3(session: aioboto3.Session = Depends(get_session)):
    async with session.client("s3", endpoint_url=settings.MINIO_ENDPOINT) as client:
        yield client


async def get_dynamodb(session: aioboto3.Session = Depends(get_session)):
    async with session.client(
        "dynamodb", endpoint_url=settings.DYNAMODB_ENDPOINT
    ) as client:
        yield client


def get_weather_service(
    s3=Depends(get_s3), dynamodb=Depends(get_dynamodb)
) -> WeatherService:
    return WeatherService(s3, dynamodb)
