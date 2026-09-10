from datetime import datetime

from pydantic import BaseModel


class WeatherResponse(BaseModel):
    id: int
    city: str
    country: str
    latitude: float
    longitude: float
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    weather: str
    description: str
    wind_speed: float
    recorded_at: datetime

    model_config = {
        "from_attributes": True
    }