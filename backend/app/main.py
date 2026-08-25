import csv
import os
from contextlib import asynccontextmanager
from math import asin, cos, radians, sin, sqrt

import httpx
import requests
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.services.itinerary_agent import generate_itinerary
from app.services.budget_forecast import forecast_budget
from app.database.connection import engine, save_weather
from app.services.nearby_service import nearby_places
from app.services.pdf_generator import generate_report
from app.services.replanner import replan_trip
from app.services.risk_engine import calculate_risk
from app.services.weather_service import fetch_weather
from app.jobs.weather_scheduler import start_weather_scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = start_weather_scheduler()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173", "http://127.0.0.1:4173", "http://localhost:4173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItineraryRequest(BaseModel):
    source_city: str = Field(min_length=2, max_length=120)
    destination_city: str = Field(min_length=2, max_length=120)
    days: int = Field(gt=0, le=30)
    budget: float = Field(gt=0)


class SosRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class WeatherRequest(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


@app.get("/")
def home():
    return {"message": "AI Travel Guardian 360"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "AI Travel Guardian 360"}


@app.get("/health/ollama")
def ollama_health():
    base_url = os.getenv("OLLAMA_BASE_URL", os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")).rstrip("/")
    try:
        response = httpx.get(f"{base_url}/api/tags", timeout=5)
        response.raise_for_status()
        models = [model.get("name", "") for model in response.json().get("models", [])]
        configured_model = os.getenv("OLLAMA_MODEL", "llama3.2")
        available = any(configured_model in model or model.startswith(configured_model.split(":")[0]) for model in models)
        return {"status": "ok" if available else "degraded", "service": "ollama", "model": configured_model, "model_available": available}
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(status_code=503, detail="Ollama is offline or unreachable.") from error


@app.get("/health/database")
def database_health():
    if engine is None:
        raise HTTPException(status_code=503, detail="Database is not configured.")
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "service": "database"}
    except Exception as error:
        raise HTTPException(status_code=503, detail="Database is unavailable.") from error


@app.post("/api/itinerary")
def itinerary(request: ItineraryRequest):
    try:
        return {"itinerary": generate_itinerary(**request.model_dump())}
    except Exception as error:
        raise HTTPException(status_code=503, detail="Ollama is unavailable. Start the local Ollama service and try again.") from error


SERVICE_LOCATIONS = {
    "hospital": {"name": "Sawai Man Singh Hospital", "latitude": 26.9005, "longitude": 75.8056, "phone": "112"},
    "police": {"name": "Ashok Nagar Police Station", "latitude": 26.9092, "longitude": 75.7956, "phone": "112"},
}


def distance_km(latitude: float, longitude: float, target: dict) -> float:
    radius = 6371
    lat_delta = radians(target["latitude"] - latitude)
    lon_delta = radians(target["longitude"] - longitude)
    value = sin(lat_delta / 2) ** 2 + cos(radians(latitude)) * cos(radians(target["latitude"])) * sin(lon_delta / 2) ** 2
    return radius * 2 * asin(sqrt(value))


@app.post("/api/sos")
def sos(request: SosRequest):
    services = []
    for service_type, location in SERVICE_LOCATIONS.items():
        services.append({**location, "type": service_type, "distance_km": round(distance_km(request.latitude, request.longitude, location), 2)})
    return {"services": services, "route_url": f"https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route={request.latitude}%2C{request.longitude}%3B{services[0]['latitude']}%2C{services[0]['longitude']}"}


@app.post("/api/weather")
def weather(request: WeatherRequest):
    try:
        response = httpx.get("https://api.open-meteo.com/v1/forecast", params={"latitude": request.latitude, "longitude": request.longitude, "daily": "temperature_2m_max,precipitation_probability_max,wind_speed_10m_max", "forecast_days": 2, "timezone": "auto"}, timeout=10)
        response.raise_for_status()
        daily = response.json()["daily"]
        tomorrow = {"date": daily["time"][1], "temperature": daily["temperature_2m_max"][1], "rain": daily["precipitation_probability_max"][1], "wind": daily["wind_speed_10m_max"][1]}
        return {"today": {"temperature": daily["temperature_2m_max"][0], "rain": daily["precipitation_probability_max"][0], "wind": daily["wind_speed_10m_max"][0]}, "tomorrow": tomorrow, "alert": "Rain expected tomorrow. Replace outdoor visit with museum visit." if tomorrow["rain"] >= 60 else "Weather looks good for outdoor plans tomorrow."}
    except (httpx.HTTPError, KeyError, IndexError) as error:
        raise HTTPException(status_code=503, detail="Weather service is temporarily unavailable.") from error


@app.get("/risk-score/{city}")
def risk_score(city: str):
    return calculate_risk(city)


@app.get("/weather/{city}")
def city_weather(city: str):
    try:
        result = fetch_weather(city)
        save_weather(result)
        return result
    except requests.RequestException as error:
        raise HTTPException(status_code=503, detail="Weather service is temporarily unavailable.") from error


@app.get("/nearby/{kind}")
def nearby(kind: str, city: str = "Jaipur"):
    if kind not in {"hospitals", "police", "pharmacy"}:
        raise HTTPException(status_code=400, detail="kind must be hospitals, police, or pharmacy")
    return {"city": city.title(), "places": nearby_places(kind, city)}


def csv_rows(filename: str) -> list[dict]:
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "database", filename))
    with open(path, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


@app.get("/scams/{city}")
def scams(city: str):
    return {"city": city.title(), "alerts": [row for row in csv_rows("scams.csv") if row["city"].lower() == city.lower()]}


@app.get("/emergency/{country}")
def emergency_contacts(country: str):
    contacts = next((row for row in csv_rows("emergency_contacts.csv") if row["country"].lower() == country.lower()), None)
    if not contacts:
        raise HTTPException(status_code=404, detail="Country not found")
    return contacts


class BudgetForecastRequest(BaseModel):
    total_spend: float = Field(ge=0)
    days_completed: int = Field(gt=0)
    total_trip_days: int = Field(gt=0)
    budget: float = Field(ge=0)


@app.get("/budget-forecast/{trip_id}")
def budget_forecast(trip_id: int, total_spend: float = 6000, days_completed: int = 3, total_trip_days: int = 6, budget: float = 10000):
    return {"trip_id": trip_id, **forecast_budget(total_spend, days_completed, total_trip_days, budget)}


class ReplanRequest(BaseModel):
    rain: float = Field(ge=0)
    threshold: float = Field(default=50, ge=0)


@app.post("/replan-trip")
def replan(request: ReplanRequest):
    return replan_trip(request.rain, request.threshold)


class ReportRequest(BaseModel):
    itinerary: str
    budget_summary: str = "No budget summary provided."
    risk_summary: str = "Risk score pending."
    emergency_contacts: str = "India emergency: police 100, ambulance 102."


@app.post("/api/trips/pdf")
def trip_pdf(request: ReportRequest):
    report = generate_report(request.itinerary, request.budget_summary, request.risk_summary, request.emergency_contacts)
    return Response(content=report.read(), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=travel-report.pdf"})