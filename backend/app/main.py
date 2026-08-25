from math import asin, cos, radians, sin, sqrt

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.services.itinerary_agent import generate_itinerary

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
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
    return {"message": "AI Travel Guardian"}


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