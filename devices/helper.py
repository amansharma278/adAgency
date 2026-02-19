import datetime

import jwt


def create_device_access_token(device):
    payload = {
        "id": device.id,
        "device_id": device.device_id,
        "exp": datetime.datetime.now() + datetime.timedelta(minutes=3 * 60),
        "iat": datetime.datetime.now(),
        "type": "access"
    }

    token = jwt.encode(payload, "SECRET_KEY12345678901234567890", algorithm="HS256")
    return token


def create_device_refresh_token(device):
    payload = {
        "id": device.id,
        "device_id": device.device_id,
        "exp": datetime.datetime.now() + datetime.timedelta(days=2),
        "iat": datetime.datetime.now(),
        "type": "refresh"
    }

    token = jwt.encode(payload, "SECRET_KEY12345678901234567890", algorithm="HS256")
    return token
