import requests
from django.conf import settings


VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
def verify_turnstile(token, remoteip=None):
    data = {
        "secret": settings.TURNSTILE_SECRET_KEY,
        "response": token
    }

    if remoteip:
        data["remoteip"] = remoteip
    response = requests.post(VERIFY_URL, data=data, timeout=10)
    response.raise_for_status()
    return bool(response.json().get("success"))

