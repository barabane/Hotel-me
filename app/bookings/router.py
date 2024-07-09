from datetime import date
from fastapi import APIRouter, Depends, Response
from app.bookings.dao import BookingsDAO
from app.bookings.schemas import SchemaBooking, SchemaBookingDatesFromTo
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.bookings.exceptions import BookingCantDelete, BookingDoesNotExists, RoomCannotBeBooked

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"]
)


@router.get("/")
async def get_all(user: Users = Depends(get_current_user)):
    return await BookingsDAO.find_user_bookings(user_id=user.id)


@router.get("/{id}")
async def get_one(id: int) -> SchemaBooking:
    return await BookingsDAO.find_by_id(id)


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    booking: SchemaBooking = await BookingsDAO.find_by_id(booking_id)
    if not booking:
        raise BookingDoesNotExists
    if booking.user_id != user.id:
        raise BookingCantDelete
    await BookingsDAO.delete(booking_id)
    return Response(status_code=204, content="Бронирование удалено")


@router.post("/add")
async def add_booking(room_id: int, dates: SchemaBookingDatesFromTo, user: Users = Depends(get_current_user)) -> SchemaBooking:
    booking: SchemaBooking | None = await BookingsDAO.add(user.id, room_id, dates.date_from, dates.date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = SchemaBooking.model_validate(booking).model_dump()
    send_booking_confirmation_email.delay(booking_dict, email_to=user.email)
    return booking
