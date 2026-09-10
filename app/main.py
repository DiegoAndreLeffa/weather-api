from fastapi import FastAPI, HTTPException

from app.services.weather_service import get_weather


app = FastAPI(
    title="Weather API",
    description="API para consulta e armazenamento de dados climáticos.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/weather/{city}")
async def weather(city: str):
    try:
        return await get_weather(city)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )