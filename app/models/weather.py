from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WeatherRecord(Base):
    __tablename__ = "weather_records"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    city: Mapped[str] = mapped_column(String(100), nullable=False)

    country: Mapped[str] = mapped_column(String(10), nullable=False)

    latitude: Mapped[float] = mapped_column(Float, nullable=False)

    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    temperature: Mapped[float] = mapped_column(Float, nullable=False)

    feels_like: Mapped[float] = mapped_column(Float, nullable=False)

    humidity: Mapped[int] = mapped_column(Integer, nullable=False)

    pressure: Mapped[int] = mapped_column(Integer, nullable=False)

    weather: Mapped[str] = mapped_column(String(50), nullable=False)

    description: Mapped[str] = mapped_column(String(100), nullable=False)

    wind_speed: Mapped[float] = mapped_column(Float, nullable=False)

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )