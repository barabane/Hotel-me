from fastapi import status

from app.exception.base import BaseException


class UserIsNotExistsException(BaseException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Такого пользователя не существует"
    
class UserDataInvalid(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Направильный логин/пароль"

class UserAlreadyExistsException(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Такой пользователь уже существует"


class TokenExpiredException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Срок действия токена истек"
