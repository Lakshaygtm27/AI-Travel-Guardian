def replan_trip(rain: float, threshold: float = 50) -> dict:
    if rain > threshold:
        return {'changed': True, 'reason': 'Rain expected', 'replace': 'Amber Fort', 'with': 'Albert Hall Museum'}
    return {'changed': False, 'reason': 'Weather is suitable for outdoor plans'}
