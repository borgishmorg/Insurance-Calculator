from datetime import datetime, timedelta
import jwt

JWT_SECRET = 'very secret secret'
ACCESS_TOKEN_EXPIRATION_TIME_MINUTES = 5
REFRESH_TOKEN_EXPIRATION_TIME_DAYS = 1


def get_access_token(user):
    payload = {
        'login': user,
        'type': 'access',
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_TIME_MINUTES)
    }
    return jwt.encode(payload=payload, key=JWT_SECRET).decode()


def get_refresh_token(user):
    payload = {
        'login': user,
        'type': 'refresh',
        'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRATION_TIME_DAYS)
    }
    return jwt.encode(payload=payload, key=JWT_SECRET).decode()

