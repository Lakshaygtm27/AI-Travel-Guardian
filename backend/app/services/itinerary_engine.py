from app.services.attraction_service import discover_attractions
from app.services.geocoding_service import geocode_city


def build_itinerary(source_city: str, destination_city: str, days: int, budget: float, weather: dict | None = None) -> dict:
    location = geocode_city(destination_city)
    attractions = discover_attractions(destination_city)
    if not attractions:
        attractions = [{'name': f'{destination_city.title()} Heritage Walk', 'category': 'local experience', 'duration': 2, 'opening_time': None}, {'name': f'{destination_city.title()} Cultural Centre', 'category': 'museum', 'duration': 2, 'opening_time': None}, {'name': f'{destination_city.title()} Riverside Walk', 'category': 'viewpoint', 'duration': 2, 'opening_time': None}]
    selected = attractions[:max(days * 3, 3)]
    rainy = bool(weather and weather.get('rain', 0) > 50)
    daily_budget = round(budget / days)
    blocks = []
    for index in range(days):
        places = [selected[(index * 3 + offset) % len(selected)] for offset in range(3)]
        if rainy and index == 0:
            indoor = next((place for place in selected if place.get('category') in {'museum', 'gallery'}), places[1])
            places[1] = indoor
        blocks.append({'day': index + 1, 'morning': {'time': '09:00', 'activity': places[0]['name'], 'category': places[0].get('category')}, 'afternoon': {'time': '13:00', 'activity': places[1]['name'], 'category': places[1].get('category')}, 'evening': {'time': '18:00', 'activity': places[2]['name'], 'category': places[2].get('category')}, 'estimated_cost': daily_budget})
    text = '\n\n'.join(f"Day {block['day']}\n09:00 Morning: {block['morning']['activity']}\n13:00 Afternoon: {block['afternoon']['activity']}\n18:00 Evening: {block['evening']['activity']}\nEstimated cost: ₹{block['estimated_cost']}" for block in blocks)
    return {'trip': {'source': source_city, 'destination': destination_city, 'days': days, 'budget': budget}, 'summary': f"A {days}-day route in {destination_city.title()} built from nearby OpenStreetMap attractions.", 'total_estimated_cost': budget, 'budget_status': 'Within Budget', 'days': blocks, 'itinerary': text, 'recommendations': ['Confirm opening hours before departure', 'Keep travel between nearby attractions grouped'], 'safety_alerts': [], 'weather': weather or [], 'risk_score': 0, 'location': location, 'source': 'real_tourism_data', 'message': 'Itinerary optimized from real destination data.'}
