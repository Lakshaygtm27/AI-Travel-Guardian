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


@app.get("/")
def home():
    return {"message": "AI Travel Guardian"}


@app.post("/api/itinerary")
def itinerary(request: ItineraryRequest):
    try:
        return {"itinerary": generate_itinerary(**request.model_dump())}
    except Exception as error:
        raise HTTPException(status_code=503, detail="Ollama is unavailable. Start the local Ollama service and try again.") from error