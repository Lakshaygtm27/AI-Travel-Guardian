import requests

CITY_COORDINATES = {'jaipur': (26.9124, 75.7873), 'delhi': (28.6139, 77.2090), 'agra': (27.1767, 78.0081)}

def nearby_places(kind: str, city: str = 'Jaipur') -> list[dict]:
    latitude, longitude = CITY_COORDINATES.get(city.lower(), CITY_COORDINATES['jaipur'])
    tag = {'hospitals': 'amenity=hospital', 'police': 'amenity=police', 'pharmacy': 'amenity=pharmacy'}[kind]
    query = f'[out:json][timeout:10];(node[{tag}](around:5000,{latitude},{longitude});way[{tag}](around:5000,{latitude},{longitude}););out center tags;'
    try:
        response = requests.post('https://overpass-api.de/api/interpreter', data=query, timeout=15)
        response.raise_for_status()
        return [{'name': item.get('tags', {}).get('name', f'Nearby {kind[:-1]}'), 'latitude': item.get('lat', item.get('center', {}).get('lat')), 'longitude': item.get('lon', item.get('center', {}).get('lon')), 'type': kind} for item in response.json().get('elements', [])[:20]]
    except requests.RequestException:
        return []
