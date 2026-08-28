from datetime import datetime, timezone
import requests

from app.services.geocoding_service import geocode_city

def fetch_weather(city: str) -> dict:
    location = geocode_city(city)
    coordinates = (location['latitude'], location['longitude'])
    response = requests.get('https://api.open-meteo.com/v1/forecast', params={'latitude': coordinates[0], 'longitude': coordinates[1], 'current': 'temperature_2m,precipitation,wind_speed_10m', 'timezone': 'auto'}, timeout=5)
    response.raise_for_status()
    current = response.json()['current']
    return {'city': city.title(), 'temperature': current['temperature_2m'], 'rain': current['precipitation'], 'wind': current['wind_speed_10m'], 'created_at': datetime.now(timezone.utc).isoformat()}
