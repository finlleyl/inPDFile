import smtplib
from pathlib import Path
from PIL import Image
from pydantic import EmailStr
from app.config import settings
from app.tasks.celery import celery
from app.tasks.email_templates import (
    create_registration_confirmation_template,
)


@celery.task
def proccess_picture(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_200_100 = image.resize((200, 100))
    image_resized_1000_500.save(f"app/static/images/resized_1000_500_{image_path.name}")
    image_resized_200_100.save(f"app/static/images/resized_200_100_{image_path.name}")


@celery.task
def send_registration_confirmation(email_to: EmailStr, code: str):
    msg_content = create_registration_confirmation_template(email_to, code)
    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
