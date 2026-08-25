import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL")


def sqlalchemy_url(database_url: str) -> str:
    parsed = urlsplit(database_url)
    query = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True) if key != "pgbouncer"]
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query), parsed.fragment))


engine = create_engine(sqlalchemy_url(DATABASE_URL), pool_pre_ping=True) if DATABASE_URL else None


def save_weather(weather: dict) -> None:
    if engine is None:
        return
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO weather_logs (city, temperature, rain, wind) VALUES (:city, :temperature, :rain, :wind)"), weather)