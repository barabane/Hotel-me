from fastapi import status

from app.exception.base import BaseException


class DateFromBiggerDateToException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Дата заезда не может быть больше даты выезда"


class TooLongBookingException(BaseException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Нельзя бронировать больше чем на 30 дней"
