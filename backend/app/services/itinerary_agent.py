import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from ollama import Client

logger = logging.getLogger("travel_guardian.itinerary")
OLLAMA_TIMEOUT_SECONDS = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "8"))


def fallback_itinerary(source_city: str, destination_city: str, days: int, budget: float) -> dict:
    activities = [("Hawa Mahal", "City Palace", "Johari Bazaar"), ("Amber Fort", "Jal Mahal", "Chokhi Dhani"), ("Albert Hall Museum", "Jantar Mantar", "Bapu Bazaar")]
    daily_budget = round(budget / days)
    day_blocks = []
    for day in range(1, days + 1):
        morning, afternoon, evening = activities[(day - 1) % len(activities)]
        day_blocks.append(f"Day {day}\nMorning: {morning}\nAfternoon: {afternoon}\nEvening: {evening}\nEstimated cost: ₹{daily_budget}")
    return {"summary": f"A {days}-day budget-conscious route from {source_city} to {destination_city}.", "total_estimated_cost": budget, "budget_status": "Within Budget", "days": day_blocks, "itinerary": "\n\n".join(day_blocks), "recommendations": ["Confirm opening hours before leaving", "Keep one indoor activity available each day"], "source": "optimized_fallback", "message": "AI generation temporarily unavailable - showing optimized fallback itinerary."}


def _call_ollama(prompt: str, model: str, host: str) -> str:
    client = Client(host=host, timeout=OLLAMA_TIMEOUT_SECONDS)
    response = client.chat(model=model, messages=[{"role": "system", "content": "You are a concise, practical travel planner. Return only the requested itinerary."}, {"role": "user", "content": prompt}], options={"num_predict": 700, "temperature": 0.2})
    return response["message"]["content"].strip()


def generate_itinerary(source_city: str, destination_city: str, days: int, budget: float) -> dict:
    started = time.perf_counter()
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    host = os.getenv("OLLAMA_BASE_URL", os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")).rstrip("/")
    prompt = f"Create a practical {days}-day itinerary from {source_city} to {destination_city} within ₹{budget:,.0f}. For every day use exactly Morning, Afternoon, and Evening lines. Keep it concise and budget-conscious."
    logger.info("[TRIP] Ollama request started model=%s host=%s", model, host)
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(_call_ollama, prompt, model, host)
    try:
        itinerary = future.result(timeout=OLLAMA_TIMEOUT_SECONDS + 2)
        elapsed = round((time.perf_counter() - started) * 1000)
        logger.info("[TRIP] Ollama response received elapsed_ms=%s", elapsed)
        return {"summary": f"AI-generated {days}-day route from {source_city} to {destination_city}.", "total_estimated_cost": budget, "budget_status": "Within Budget", "days": itinerary.split("\n\n"), "itinerary": itinerary, "recommendations": [], "source": "ollama", "message": "AI itinerary generated successfully."}
    except Exception as error:
        elapsed = round((time.perf_counter() - started) * 1000)
        logger.warning("[TRIP] Ollama unavailable; fallback selected elapsed_ms=%s error=%s", elapsed, type(error).__name__)
        return fallback_itinerary(source_city, destination_city, days, budget)
    finally:
        executor.shutdown(wait=False, cancel_futures=True)