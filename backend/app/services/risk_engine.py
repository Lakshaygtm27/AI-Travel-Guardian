RISK_FACTORS = {'weather': 20, 'medical': 10, 'crowd': 15, 'transport': 12, 'scam': 8}

def calculate_risk(city: str) -> dict:
    score = sum(RISK_FACTORS.values())
    level = 'Low' if score < 40 else 'Medium' if score < 70 else 'High'
    return {'city': city.title(), 'risk_score': score, 'risk_level': level, 'factors': RISK_FACTORS}
