import os

from ollama import Client


def generate_itinerary(source_city: str, destination_city: str, days: int, budget: float) -> str:
    client = Client(host=os.getenv("OLLAMA_BASE_URL", os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")))
    prompt = f"""Create a practical {days}-day travel itinerary from {source_city} to {destination_city} with a total budget of ₹{budget:,.0f}.
Use exactly this structure for every day:
Day N

Morning:
activity

Afternoon:
activity

Evening:
activity

Keep activities realistic, mention budget-conscious choices, and return only the itinerary."""
    response = client.chat(
        model=os.getenv("OLLAMA_MODEL", "llama3.2"),
        messages=[
            {"role": "system", "content": "You are a concise, practical travel planner."},
            {"role": "user", "content": prompt},
        ],
    )
    return response["message"]["content"].strip()