from datetime import date

from sqlalchemy import func, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.utils.get_booked_rooms import get_booked_rooms


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_not_empty_hotels(cls, location: str, date_from: date, date_to: date):
        booked_rooms = get_booked_rooms(date_from, date_to)
        not_empty_hotels = select(
            Hotels.id,
            Hotels.name,
            Hotels.location,
            Hotels.services,
            Hotels.rooms_quantity,
            Hotels.image_id,
            (Hotels.rooms_quantity -
             func.coalesce(booked_rooms.c.booked_rooms,
                           0)).label("rooms_left")
        ).join(booked_rooms, Hotels.__table__.c.id == booked_rooms.c.hotel_id, isouter=True).where(Hotels.location.like(f"%{location}%"))

        async with async_session_maker() as session:
            res = await session.execute(not_empty_hotels)
            return res.mappings().all()

    @classmethod
    async def find_hotel_rooms(cls, hotel_id: int, date_from: date, date_to: date):
        booked_rooms = get_booked_rooms(date_from, date_to)
        hotel_rooms = select(
            Rooms.id,
            Rooms.hotel_id,
            Rooms.name,
            Rooms.description,
            Rooms.price,
            Rooms.services,
            Rooms.quantity,
            Rooms.image_id,
            (Rooms.price * (date_to.day - date_from.day)).label("total_cost"),
            (Rooms.__table__.c.quantity -
             func.coalesce(booked_rooms.c.booked_rooms, 0)).label("rooms_left")
        ).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).join(
            Hotels, Hotels.id == Rooms.hotel_id
        ).where(
            Rooms.hotel_id == hotel_id
        ).group_by(
            Rooms.id,
            booked_rooms.table_valued()
        )

        async with async_session_maker() as session:
            res = await session.execute(hotel_rooms)
            return res.mappings().all()
