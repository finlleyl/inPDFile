from pathlib import Path
from PIL import Image
from app.tasks.celery import celery


@celery.task
def proccess_picture(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized_1000_500 = image.resize((1000, 500))
    image_resized_200_100 = image.resize((200, 100))
    image_resized_1000_500.save(f"app/static/images/resized_1000_500_{image_path.name}")
    image_resized_200_100.save(f"app/static/images/resized_200_100_{image_path.name}")
