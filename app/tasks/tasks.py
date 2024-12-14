import smtplib
from time import sleep
from pydantic import EmailStr
from app.tasks.celery import celery
from PIL import Image
from pathlib import Path
from app.config import settings

@celery.task
def proccess_picture(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_200_100 = image.resize((200, 100))
    image_resized_1000_500.save(f"app/static/images/resized_1000_500_{image_path.name}")
    image_resized_200_100.save(f"app/static/images/resized_200_100_{image_path.name}")


@celery.task
def send_booking_confirmation_email(: dict, email_to: EmailStr):
    email_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(
        , "email"
    )
    sleep(10)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)


