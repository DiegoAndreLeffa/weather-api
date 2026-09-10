from datetime import datetime

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.exceptions.weather import (
    CityNotFoundError,
    WeatherServiceError,
)
from app.models.weather import WeatherRecord


GEOCODING_URL = "https://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


async def get_city_coordinates(city: str):
    params = {
        "q": city,
        "limit": 1,
        "appid": settings.openweather_api_key,
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                GEOCODING_URL,
                params=params,
            )

        response.raise_for_status()

    except httpx.HTTPError as error:
        raise WeatherServiceError(
            "Erro ao consultar o serviço de geocoding."
        ) from error

    data = response.json()

    if not data:
        raise CityNotFoundError(
            f"Cidade '{city}' não encontrada."
        )

    return data[0]


async def get_weather(city: str, db: Session):
    location = await get_city_coordinates(city)

    params = {
        "lat": location["lat"],
        "lon": location["lon"],
        "appid": settings.openweather_api_key,
        "units": "metric",
        "lang": "pt_br",
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(
                WEATHER_URL,
                params=params,
            )

        response.raise_for_status()

    except httpx.HTTPError as error:
        raise WeatherServiceError(
            "Erro ao consultar o serviço de clima."
        ) from error

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
        recorded_at=datetime.now(),
    )

    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)

    return weather_record