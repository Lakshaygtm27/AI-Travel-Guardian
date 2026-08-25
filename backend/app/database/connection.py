import os

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


def save_weather(weather: dict) -> None:
    if engine is None:
        return
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO weather_logs (city, temperature, rain, wind) VALUES (:city, :temperature, :rain, :wind)"), weather)