from pathlib import Path
from smtplib import SMTP_SSL

from PIL import Image
from pydantic import EmailStr

from app.tasks.celery_config import celery_app as celery
from app.tasks.email_templates import (create_booking_confirmation_template,
                                       recover_email_template,
                                       registry_confirmation_template)
from config import settings


@celery.task
def process_pic(path: str):
    img_path = Path(path)
    img = Image.open(img_path)
    img_resized_1000_500 = img.resize((1000, 500))
    img_resized_200_100 = img.resize((200, 100))
    img_resized_1000_500.save(
        f"app/static/images/resized_1000_500_{img_path.name}")
    img_resized_200_100.save(
        f"app/static/images/resized_200_100_{img_path.name}")


@celery.task
def send_booking_confirmation_email(booking: dict, email_to: EmailStr):
    msg_content = create_booking_confirmation_template(
        booking=booking, email_to=email_to)
    with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def confirm_registry(email_to: EmailStr):
    msg_content = registry_confirmation_template(email_to)
    with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


@celery.task
def send_recover_email(email_to: EmailStr, access_token):
    msg_content = recover_email_template(email_to, access_token)
    with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
