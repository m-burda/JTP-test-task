import datetime

from pydantic import BaseModel, model_serializer


class WeatherLogData(BaseModel):
    city: str
    timestamp: datetime.datetime
    s3_path: str

    @model_serializer
    def serialize(self):
        return {
                    'city': {'S': self.city.lower()},
                    'timestamp': {'S': self.timestamp.isoformat()},
                    's3_path': {'S': self.s3_path}
                }