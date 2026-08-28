import time
import requests

_cache: dict[str, tuple[float, dict]] = {}
CACHE_SECONDS = 86400

def geocode_city(city: str) -> dict:
    key = city.strip().lower()
    cached = _cache.get(key)
    if cached and time.time() - cached[0] < CACHE_SECONDS:
        return cached[1]
    response = requests.get('https://nominatim.openstreetmap.org/search', params={'q': f'{city}, India', 'format': 'jsonv2', 'limit': 1}, headers={'User-Agent': 'AI-Travel-Guardian-360/1.0'}, timeout=3)
    response.raise_for_status()
    results = response.json()
    if not results:
        raise ValueError(f'Could not locate Indian city: {city}')
    location = {'city': city.title(), 'latitude': float(results[0]['lat']), 'longitude': float(results[0]['lon']), 'display_name': results[0].get('display_name', city.title())}
    _cache[key] = (time.time(), location)
    return location
