import time
import requests
from app.services.geocoding_service import geocode_city

_cache: dict[str, tuple[float, list[dict]]] = {}
CACHE_SECONDS = 86400


def discover_attractions(city: str) -> list[dict]:
    key = city.strip().lower()
    cached = _cache.get(key)
    if cached and time.time() - cached[0] < CACHE_SECONDS:
        return cached[1]
    location = geocode_city(city)
    query = f'''[out:json][timeout:12];(nwr["tourism"~"attraction|museum|viewpoint"](around:20000,{location["latitude"]},{location["longitude"]});nwr["historic"](around:20000,{location["latitude"]},{location["longitude"]});nwr["leisure"="park"](around:20000,{location["latitude"]},{location["longitude"]}););out center tags;'''
    try:
        response = requests.post('https://overpass-api.de/api/interpreter', data={'data': query}, headers={'User-Agent': 'AI-Travel-Guardian-360/1.0', 'Accept': 'application/json'}, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        _cache[key] = (time.time(), [])
        return []
    attractions = []
    seen = set()
    for item in response.json().get('elements', []):
        tags = item.get('tags', {})
        name = tags.get('name')
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        center = item.get('center', {})
        attractions.append({'name': name, 'category': tags.get('tourism') or tags.get('historic') or tags.get('leisure') or 'attraction', 'rating': None, 'entry_fee': None, 'duration': 2, 'latitude': item.get('lat', center.get('lat')), 'longitude': item.get('lon', center.get('lon')), 'opening_time': tags.get('opening_hours'), 'closing_time': None})
    attractions.sort(key=lambda place: (place['rating'] is None, place['name']))
    _cache[key] = (time.time(), attractions[:30])
    return _cache[key][1]
