from smtplib import SMTP_SSL
from app.bookings.schemas import SchemaBooking
from app.tasks.celery_config import celery_app as celery
from app.tasks.email_templates import checkin_reminder_template
from config import settings
from datetime import date, timedelta
from app.bookings.dao import BookingsDAO
from app.users.dao import UserDAO
from asgiref.sync import async_to_sync


@celery.task(name="tomorrow_checkin_reminder")
def tomorrow_checkin_reminder():
    bookings = async_to_sync(BookingsDAO.find_all)()
    for booking in bookings:
        if booking.date_from - date.today() == timedelta(1):
            user = async_to_sync(
                UserDAO.find_by_id)(booking.user_id)
            booking_dict = SchemaBooking.model_validate(booking).model_dump()
            msg_content = checkin_reminder_template(
                booking_dict, user.email, 1)
            with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(msg_content)
                return True
    return False


@celery.task(name="three_days_checkin_reminder")
def three_days_checkin_reminder():
    bookings = async_to_sync(BookingsDAO.find_all)()
    for booking in bookings:
        if booking.date_from - date.today() == timedelta(3):
            user = async_to_sync(
                UserDAO.find_by_id)(booking.user_id)
            booking_dict = SchemaBooking.model_validate(booking).model_dump()
            msg_content = checkin_reminder_template(
                booking_dict, user.email, 3)
            with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(msg_content)
                return True
    return False
