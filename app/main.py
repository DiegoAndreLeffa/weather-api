from fastapi import Depends, FastAPI, HTTPException, Query, Path
from sqlalchemy.orm import Session
from sqlalchemy import text

from typing import Optional
from sqlalchemy import select

from app.database.connection import engine, get_db
from app.database.init_db import init_database
from app.services.weather_service import get_weather
from app.schemas.weather import WeatherResponse
from app.models.weather import WeatherRecord

from app.exceptions.weather import CityNotFoundError, WeatherServiceError


init_database()


app = FastAPI(
    title="Weather API",
    description="API para consulta e armazenamento de dados climáticos.",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(error),
        }
        
        
@app.get(
    "/api/v1/weather/{city}",
    response_model=WeatherResponse,
)
async def weather(
    city: str = Path(
        min_length=2,
        max_length=100,
    ),
    db: Session = Depends(get_db),
):
    try:
        return await get_weather(city, db)

    except CityNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except WeatherServiceError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error),
        )
        
        
@app.get(
    "/api/v1/weather",
    response_model=list[WeatherResponse],
)
def weather_history(
    city: Optional[str] = None,
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):
    query = select(WeatherRecord)

    if city:
        query = query.where(
            WeatherRecord.city.ilike(f"%{city}%")
        )

    query = query.order_by(
        WeatherRecord.recorded_at.desc()
    ).limit(limit)

    result = db.execute(query)

    return result.scalars().all()

@app.get(
    "/api/v1/weather/id/{weather_id}",
    response_model=WeatherResponse,
)
def get_weather_by_id(
    weather_id: int,
    db: Session = Depends(get_db),
):
    weather_record = db.get(
        WeatherRecord,
        weather_id,
    )

    if weather_record is None:
        raise HTTPException(
            status_code=404,
            detail="Registro não encontrado.",
        )

    return weather_record