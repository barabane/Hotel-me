from datetime import UTC, datetime

from fastapi import Depends, Request
from jose import JWTError, jwt

from app.users.dao import UserDAO
from app.users.exceptions import TokenExpiredException, UserIsNotExistsException
from config import settings


def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise TokenExpiredException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_HASH, settings.HASH_METHOD)
    except JWTError:
        raise TokenExpiredException
    expire: str = payload.get("exp")
    if (not expire) or expire < datetime.now(UTC).timestamp():
        raise TokenExpiredException
    user_id: str = payload.get("sub")
    if not user_id:
        raise TokenExpiredException
    user = await UserDAO.find_by_id(int(user_id))
    if not user:
        raise UserIsNotExistsException

    return user
