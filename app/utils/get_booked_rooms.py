from sqlalchemy import and_, func, select

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


def get_booked_rooms(date_from, date_to):
    booked_rooms = select(
        Rooms.hotel_id, (Rooms.id).label("room_id"), func.count(Rooms.id).label("booked_rooms")).select_from(Hotels).join(
        Rooms, Hotels.id == Rooms.hotel_id, isouter=True).join(Bookings, Rooms.id == Bookings.room_id, isouter=True).where(
        and_(
            Bookings.date_from <= date_to,
            Bookings.date_from > date_from
        )
    ).group_by(Rooms.id, Rooms.hotel_id).cte("booked_rooms")
    return booked_rooms
