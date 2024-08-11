from jose import jwt

from config import settings


def decode_jwt(token: str):
    payload = jwt.decode(token, settings.SECRET_HASH, settings.HASH_METHOD)
    return payload
