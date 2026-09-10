import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.weather import WeatherRecord


GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_city_coordinates(city: str):
    params = {
        "q": city,
        "limit": 1,
        "appid": settings.openweather_api_key,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            GEOCODING_URL,
            params=params,
        )

    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    return data[0]


async def get_weather(city: str, db: Session):
    location = await get_city_coordinates(city)

    if location is None:
        return None

    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "appid": settings.openweather_api_key,
        "units": "metric",
        "lang": "pt_br",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            WEATHER_URL,
            params=params,
        )

    response.raise_for_status()

    data = response.json()

    weather_record = WeatherRecord(
        city=data["name"],
        country=data["sys"]["country"],
        latitude=data["coord"]["lat"],
        longitude=data["coord"]["lon"],
        temperature=data["main"]["temp"],
        feels_like=data["main"]["feels_like"],
        humidity=data["main"]["humidity"],
        pressure=data["main"]["pressure"],
        weather=data["weather"][0]["main"],
        description=data["weather"][0]["description"],
        wind_speed=data["wind"]["speed"],
        recorded_at=__import__("datetime").datetime.now(),
    )

    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    return weather_record