from datetime import datetime, timezone
import requests

CITY_COORDINATES = {'jaipur': (26.9124, 75.7873), 'delhi': (28.6139, 77.2090), 'agra': (27.1767, 78.0081), 'mumbai': (19.0760, 72.8777)}

def fetch_weather(city: str) -> dict:
    coordinates = CITY_COORDINATES.get(city.lower(), CITY_COORDINATES['jaipur'])
    response = requests.get('https://api.open-meteo.com/v1/forecast', params={'latitude': coordinates[0], 'longitude': coordinates[1], 'current': 'temperature_2m,precipitation,wind_speed_10m', 'timezone': 'auto'}, timeout=10)
    response.raise_for_status()
    current = response.json()['current']
    return {'city': city.title(), 'temperature': current['temperature_2m'], 'rain': current['precipitation'], 'wind': current['wind_speed_10m'], 'created_at': datetime.now(timezone.utc).isoformat()}
