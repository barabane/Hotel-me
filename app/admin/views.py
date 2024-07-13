from sqladmin import ModelView
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [Users.id, Users.email]
    column_details_list = [Users.id, Users.email, Users.booking]
    can_delete = False


class HotelsAdmin(ModelView, model=Hotels):
    name = "Отель"
    name_plural = "Отели"
    column_list = "__all__"
    column_details_list = "__all__"


class BookingsAdmin(ModelView, model=Bookings):
    name = "Бронь"
    name_plural = "Брони"
    column_list = "__all__"
    column_details_list = "__all__"


class RoomsAdmin(ModelView, model=Rooms):
    name = "Комната"
    name_plural = "Комнаты"
    column_list = "__all__"
    column_details_list = "__all__"
