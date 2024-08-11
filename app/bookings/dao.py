from datetime import date

from sqlalchemy import func, insert, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker, nullpool_session_maker
from app.hotels.rooms.models import Rooms
from app.utils.get_booked_rooms import get_booked_rooms


class BookingsDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(
            cls,
            user_id: int,
            room_id: int,
            date_from: date,
            date_to: date
    ):
        booked_rooms = get_booked_rooms(date_from, date_to)
        get_rooms_left = select(
            (Rooms.quantity - func.count(booked_rooms.c.room_id))
        ).select_from(Rooms).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).where(Rooms.id == room_id).group_by(
            Rooms.quantity, booked_rooms.c.room_id
        )

        async with async_session_maker() as session:
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(
                    user_id=user_id,
                    room_id=room_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price
                ).returning(
                    Bookings.id,
                    Bookings.user_id,
                    Bookings.room_id,
                    Bookings.date_from,
                    Bookings.date_to,
                    Bookings.price,
                    Bookings.total_days,
                    Bookings.total_cost
                )
                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one()
            else:
                return None

    @classmethod
    async def find_user_bookings(cls, user_id: int):
        user_bookings = select(Bookings).where(
            Bookings.user_id == user_id).cte("user_bookings")

        bookings_with_room_info = select(
            user_bookings, Rooms.image_id, Rooms.name, Rooms.description, Rooms.services
        ).join(Rooms, isouter=True).where(user_bookings.c.user_id == user_id)

        async with async_session_maker() as session:
            res = await session.execute(bookings_with_room_info)
            return res.mappings().all()

    @classmethod
    async def find_all_nullpool(cls):
        async with nullpool_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
