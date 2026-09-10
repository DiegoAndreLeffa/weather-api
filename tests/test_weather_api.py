from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_weather_history_invalid_limit():
    response = client.get(
        "/api/v1/weather?limit=-1"
    )

    assert response.status_code == 422