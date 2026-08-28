import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from ollama import Client
from app.services.itinerary_engine import build_itinerary
from app.services.weather_service import fetch_weather

logger = logging.getLogger("travel_guardian.itinerary")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "5"))


def fallback_itinerary(source_city: str, destination_city: str, days: int, budget: float, weather: dict | None = None) -> dict:
    try:
        result = build_itinerary(source_city, destination_city, days, budget, weather)
    except Exception as error:
        logger.warning("[TRIP] Destination fallback data unavailable error=%s", type(error).__name__)
        daily_budget = round(budget / days)
        blocks = []
        for day in range(1, days + 1):
            blocks.append(f"Day {day}\n09:00 Morning: {destination_city.title()} local highlights\n13:00 Afternoon: {destination_city.title()} cultural experience\n18:00 Evening: {destination_city.title()} evening market\nEstimated cost: ₹{daily_budget}")
        result = {"trip": {"source": source_city, "destination": destination_city, "days": days, "budget": budget}, "summary": f"A {days}-day route in {destination_city.title()}.", "total_estimated_cost": budget, "budget_status": "Within Budget", "days": blocks, "itinerary": "\n\n".join(blocks), "recommendations": [], "safety_alerts": [], "weather": weather or [], "risk_score": 0}
    result['source'] = 'optimized_fallback'
    result['message'] = 'AI generation temporarily unavailable - showing optimized itinerary from real destination data.'
    return result


def _call_ollama(prompt: str, model: str, host: str) -> str:
    client = Client(host=host, timeout=OLLAMA_TIMEOUT_SECONDS)
    response = client.chat(model=model, messages=[{"role": "system", "content": "You are a concise, practical travel planner. Return only the requested itinerary."}, {"role": "user", "content": prompt}], options={"num_predict": 700, "temperature": 0.2})
    return response["message"]["content"].strip()


def generate_itinerary(source_city: str, destination_city: str, days: int, budget: float) -> dict:
    started = time.perf_counter()
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    host = os.getenv("OLLAMA_BASE_URL", os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")).rstrip("/")
    data_executor = ThreadPoolExecutor(max_workers=2)
    weather_future = data_executor.submit(fetch_weather, destination_city)
    destination_future = data_executor.submit(build_itinerary, source_city, destination_city, days, budget, None)
    try:
        weather = weather_future.result(timeout=6)
    except Exception as error:
        logger.warning("[TRIP] Weather lookup skipped error=%s", type(error).__name__)
        weather = None
    try:
        destination_data = destination_future.result(timeout=6)
        places = [daypart['activity'] for day in destination_data['days'] for daypart in (day['morning'], day['afternoon'], day['evening'])]
    except Exception as error:
        logger.warning("[TRIP] Destination discovery skipped error=%s", type(error).__name__)
        destination_data = None
        places = [f'{destination_city.title()} Heritage Walk', f'{destination_city.title()} Cultural Centre', f'{destination_city.title()} Riverside Viewpoint']
    finally:
        data_executor.shutdown(wait=False, cancel_futures=True)
    context = ', '.join(dict.fromkeys(places))[:1200]
    prompt = f"Create a practical {days}-day itinerary from {source_city} to {destination_city} within ₹{budget:,.0f}. Use only these discovered destination places where possible: {context}. For every day use exactly Morning, Afternoon, and Evening lines. Keep it concise and budget-conscious."
    logger.info("[TRIP] Ollama request started model=%s host=%s", model, host)
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_call_ollama, prompt, model, host)
    try:
        itinerary = future.result(timeout=OLLAMA_TIMEOUT_SECONDS + 1)
        elapsed = round((time.perf_counter() - started) * 1000)
        logger.info("[TRIP] Ollama response received elapsed_ms=%s", elapsed)
        return {"trip": {"source": source_city, "destination": destination_city, "days": days, "budget": budget}, "summary": f"AI-generated {days}-day route from {source_city} to {destination_city}.", "total_estimated_cost": budget, "budget_status": "Within Budget", "days": itinerary.split("\n\n"), "itinerary": itinerary, "recommendations": [], "safety_alerts": [], "weather": weather or [], "risk_score": 0, "source": "ollama", "message": "AI itinerary generated successfully."}
    except Exception as error:
        elapsed = round((time.perf_counter() - started) * 1000)
        logger.warning("[TRIP] Ollama unavailable; fallback selected elapsed_ms=%s error=%s", elapsed, type(error).__name__)
        if destination_data is not None:
            destination_data['source'] = 'optimized_fallback'
            destination_data['message'] = 'AI generation temporarily unavailable - showing optimized itinerary from real destination data.'
            return destination_data
        return fallback_itinerary(source_city, destination_city, days, budget, weather)
    finally:
        executor.shutdown(wait=False, cancel_futures=True)