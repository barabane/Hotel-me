from fastapi import status
from app.exception.base import BaseException


class RoomCannotBeBooked(BaseException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Не осталось свободных номеров"


class BookingDoesNotExists(BaseException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такого бронирования не существует"


class BookingCantDelete(BaseException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Вы не можете удалить это бронирование"
