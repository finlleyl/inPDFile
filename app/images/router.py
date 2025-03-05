import shutil
from fastapi import UploadFile
from fastapi import APIRouter

from app.tasks.tasks import proccess_picture


router = APIRouter(prefix="/images", tags=["Загрузка изображения"])


@router.post("/avatar")
async def add_avatar_image(name: int, file: UploadFile):
    image_path = f"app/static/images/{name}.webp"
    with open(image_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    proccess_picture.delay(image_path)
