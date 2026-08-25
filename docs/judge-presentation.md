# AI Travel Guardian: Judge Presentation

## 1. Problem
Travelers make decisions across disconnected apps while risk, budget, weather, and emergency context change during a trip.

## 2. Solution
A travel command center that turns one trip request into a living, safety-aware plan.

## 3. Architecture
React/Vite and Leaflet frontend; FastAPI services; PostgreSQL/Supabase data; Open-Meteo and Overpass live sources; Ollama itinerary generation; n8n automation.

## 4. AI Agents
Itinerary generation, weather-aware replanning, budget forecasting, and the travel desk chatbot.

## 5. Live Dashboard
Command Center shows budget, weather, risk, safety, map layers, alerts, forecast, and recommendations.

## 6. SOS Feature
Browser GPS finds nearby hospitals and police and opens an OpenStreetMap route.

## 7. Risk Intelligence
Transparent weighted risk score: weather 20, medical 10, crowd 15, transport 12, scam 8 = 65 Medium.

## 8. n8n Automation
Trip creation, weather alerts, budget thresholds, and completed-trip journals become visible workflows.

## 9. Impact
Less decision friction, faster emergency response, and practical local safety context.

## 10. Future Roadmap
Supabase production rollout, authenticated traveler profiles, provider-backed booking, and hosted AI inference.
