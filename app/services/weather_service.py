import httpx

from app.core.config import settings


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


async def get_weather(city: str):
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

    return response.json()