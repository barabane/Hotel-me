from app.bookings.dao import BookingsDAO
from datetime import datetime


async def test_add_and_get_booking():
    new_booking = await BookingsDAO.add(
        user_id=1,
        room_id=1,
        date_from=datetime.strptime("2024-07-10", "%Y-%m-%d"),
        date_to=datetime.strptime("2024-07-25", "%Y-%m-%d")
    )

    new_booking = await BookingsDAO.find_by_id(new_booking.id)

    assert new_booking
