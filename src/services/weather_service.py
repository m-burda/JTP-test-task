from datetime import datetime, timedelta, timezone
from http import HTTPStatus
import json
from typing import Optional, Any
import httpx
from botocore.exceptions import ClientError
from fastapi import HTTPException

from application.config import settings
from application.models import WeatherLogData


class WeatherService:
    def __init__(self, s3, dynamodb):
        self.s3 = s3
        self.dynamodb = dynamodb

    async def get_weather(self, city: str) -> dict[str, Any]:
        cached_data = await self.get_cached_weather(city)
        if cached_data:
            return cached_data

        weather_data = await self.fetch_weather(city)
        s3_path = await self.store_weather_data(city, weather_data)

        weather_log = WeatherLogData(
            city=city, timestamp=datetime.now(timezone.utc), s3_path=s3_path
        )
        await self.log_to_dynamodb(weather_log)

        return weather_data

    async def get_cached_weather(self, city: str) -> Optional[dict[str, Any]]:
        now = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        try:
            response = await self.s3.get_object(
                Bucket=settings.BUCKET_NAME,
                Key=f"{city.lower()}_{now.isoformat()}.json",
            )
            if response["Expires"] < now - timedelta(
                minutes=settings.OBJECT_EXPIRY_MINUTES
            ):
                return
            data = await response["Body"].read()
            return json.loads(data)
        except ClientError:
            return

    @staticmethod
    async def fetch_weather(city: str) -> dict[str, Any]:
        async with httpx.AsyncClient() as client:
            params = {
                "q": city,
                "appid": settings.OPENWEATHER_API_KEY,
                "units": "metric",
            }
            response = await client.get(settings.OPENWEATHER_BASE_URL, params=params)
            if response.status_code != HTTPStatus.OK:
                raise HTTPException(
                    status_code=500, detail="Failed to fetch weather data"
                )

            return response.json()

    async def store_weather_data(self, city: str, weather_data: dict) -> str:
        now = datetime.now(timezone.utc)

        s3_path = f"{city.lower()}_{now.replace(minute=0, second=0, microsecond=0).isoformat()}.json"

        await self.s3.put_object(
            Bucket=settings.BUCKET_NAME,
            Key=s3_path,
            Body=json.dumps(weather_data),
            Expires=now + timedelta(minutes=settings.OBJECT_EXPIRY_MINUTES),
        )
        return s3_path

    async def log_to_dynamodb(self, weather_data: WeatherLogData):
        await self.dynamodb.put_item(
            TableName=settings.DYNAMODB_TABLE_NAME, Item=weather_data.model_dump()
        )
