def forecast_budget(total_spend: float, days_completed: int, total_trip_days: int, budget: float) -> dict:
    daily_average = total_spend / max(days_completed, 1)
    forecast = daily_average * total_trip_days
    return {'current_spend': total_spend, 'forecast': round(forecast, 2), 'budget': budget, 'status': 'Over Budget' if forecast > budget else 'On Track'}
