from datetime import datetime

import requests


def is_weekday():
    weekend = [5, 6]
    return datetime.today().weekday() not in weekend


def get_holidays():
    r = requests.get("http://localhost/api/holidays")
    if r.status_code == 200:
        return r.json()
    return None
