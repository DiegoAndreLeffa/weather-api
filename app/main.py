from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.connection import engine, get_db
from app.database.init_db import init_database
from app.services.weather_service import get_weather


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
        
        
@app.get("/weather/{city}")
async def weather(
    city: str,
    db: Session = Depends(get_db),
):
    try:
        result = await get_weather(city, db)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Cidade não encontrada.",
            )

        return result

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )