from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from application.dependencies import get_weather_service
from application.helpers import setup_storage
from services.weather_service import WeatherService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_storage()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/weather")
async def get_weather(
    city: str, service: WeatherService = Depends(get_weather_service)
):
    return await service.get_weather(city)
