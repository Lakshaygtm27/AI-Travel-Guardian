from apscheduler.schedulers.background import BackgroundScheduler
from app.database.connection import save_weather
from app.services.weather_service import fetch_weather

def start_weather_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: save_weather(fetch_weather('Jaipur')), 'interval', minutes=15, id='jaipur-weather', replace_existing=True)
    scheduler.start()
    return scheduler
