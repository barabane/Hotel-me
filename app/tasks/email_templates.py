from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите бронирование</h1>
            Вы забронировали отель с {booking['date_from']} по {booking['date_to']}
        """,
        subtype="html",
    )
    return email


def registry_confirmation_template(email_to: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Регистрация на сайте"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Подтвердите регистрацию на сайте</h1>
        """,
        subtype="html",
    )
    return email


def checkin_reminder_template(booking: dict, email_to: EmailStr, days: int):
    email = EmailMessage()
    email["Subject"] = f"Осталось дней до заселения: {days}"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Напоминание о бронировании</h1>
            <p>Вы забронировали отель с {booking['date_from']} по {booking['date_to']}</p>
        """,
        subtype="html",
    )
    return email


def recover_email_template(email_to: EmailStr, access_token):
    email = EmailMessage()
    email["Subject"] = f"Восстановление пароля"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Восстановление пароля</h1>
            <p>Перейдите по ссылке для восстановления пароля http://127.0.0.1:8000/pages/recover?access_token={access_token}</p>
        """,
        subtype="html",
    )
    return email
