from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.exceptions.weather import CityNotFoundError
from app.services.weather_service import get_city_coordinates, get_weather


@pytest.mark.asyncio
async def test_get_city_coordinates():
    mock_response = MagicMock()

    mock_response.raise_for_status.return_value = None

    mock_response.json.return_value = [
        {
            "name": "Florianópolis",
            "lat": -27.5973,
            "lon": -48.5496,
            "country": "BR",
        }
    ]

    with patch(
        "app.services.weather_service.httpx.AsyncClient"
    ) as mock_client:

        mock_client.return_value.__aenter__.return_value.get = (
            AsyncMock(return_value=mock_response)
        )

        result = await get_city_coordinates(
            "Florianopolis"
        )

    assert result["name"] == "Florianópolis"
    assert result["country"] == "BR"
    assert result["lat"] == -27.5973
    assert result["lon"] == -48.5496


@pytest.mark.asyncio
async def test_get_city_coordinates_city_not_found():
    mock_response = MagicMock()

    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = []

    with patch(
        "app.services.weather_service.httpx.AsyncClient"
    ) as mock_client:

        mock_client.return_value.__aenter__.return_value.get = (
            AsyncMock(return_value=mock_response)
        )

        with pytest.raises(CityNotFoundError):
            await get_city_coordinates(
                "CidadeQueNaoExiste"
            )
            
            
@pytest.mark.asyncio
async def test_get_weather():
    mock_response = MagicMock()

    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "name": "Florianópolis",
        "sys": {
            "country": "BR",
        },
        "coord": {
            "lat": -27.5973,
            "lon": -48.5496,
        },
        "main": {
            "temp": 20.5,
            "feels_like": 20.0,
            "humidity": 87,
            "pressure": 1015,
        },
        "weather": [
            {
                "main": "Clouds",
                "description": "nublado",
            }
        ],
        "wind": {
            "speed": 2.5,
        },
    }

    mock_db = MagicMock()

    with patch(
        "app.services.weather_service.get_city_coordinates"
    ) as mock_coordinates:

        mock_coordinates.return_value = {
            "name": "Florianópolis",
            "lat": -27.5973,
            "lon": -48.5496,
            "country": "BR",
        }

        with patch(
            "app.services.weather_service.httpx.AsyncClient"
        ) as mock_client:

            mock_client.return_value.__aenter__.return_value.get = (
                AsyncMock(return_value=mock_response)
            )

            result = await get_weather(
                "Florianopolis",
                mock_db,
            )

    assert result.city == "Florianópolis"
    assert result.country == "BR"
    assert result.latitude == -27.5973
    assert result.longitude == -48.5496
    assert result.temperature == 20.5
    assert result.humidity == 87

    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()