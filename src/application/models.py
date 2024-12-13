import datetime
from uuid import uuid4, UUID

from pydantic import BaseModel, model_serializer, Field


class WeatherLogData(BaseModel):
    id: UUID = Field(default_factory=uuid4, frozen=True)
    city: str
    timestamp: datetime.datetime
    s3_path: str

    @model_serializer
    def serialize(self):
        return {
            "id": {"S": str(self.id)},
            "city": {"S": self.city.lower()},
            "timestamp": {"S": self.timestamp.isoformat()},
            "s3_path": {"S": self.s3_path},
        }
