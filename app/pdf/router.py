from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from app.exceptions import FileNotPDFException
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from fastapi.responses import StreamingResponse
from app.users.dependencies import get_current_user
from app.users.models import Users
import io
import re
import urllib

router = APIRouter(
    prefix="/pdf",
    tags=["Pdf"],
)


@router.post("/upload")
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...),
    user: Users = Depends(get_current_user),
):
    if file.content_type != "application/pdf":
        raise FileNotPDFException

    db = request.app.mongodb
    fs = AsyncIOMotorGridFSBucket(db)

    file_id = await fs.upload_from_stream(
        file.filename,
        file.file,
        metadata={
            "user_id": user.id,
            "content_type": file.content_type,
            "timestamp": datetime.now(),
        },
    )

    return {"file_id": str(file_id)}


@router.get("/dowload/{file_id}")
async def download_pdf(file_id: str, request: Request):
    fs = AsyncIOMotorGridFSBucket(request.app.mongodb)

    try:
        file_id = ObjectId(file_id)
        grid_out = await fs.open_download_stream(file_id)
        content = await grid_out.read()

        # Получение имени файла из метаданных или использование default.pdf
        filename = grid_out.filename or "default.pdf"

        # Проверка на наличие нелатинских символов
        if re.search(r"[^a-zA-Z0-9._-]", filename):
            # Кодирование имени файла
            filename_encoded = urllib.parse.quote(filename)
            content_disposition = f"attachment; filename*=UTF-8''{filename_encoded}"
        else:
            content_disposition = f'attachment; filename="{filename}"'

        return StreamingResponse(
            io.BytesIO(content),
            media_type="application/pdf",
            headers={"Content-Disposition": content_disposition},
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/all_files/")
async def list_files(request: Request):
    try:
        db = request.app.mongodb
        fs = AsyncIOMotorGridFSBucket(db)
        # Извлечение всех документов из коллекции fs.files
        cursor = fs.find({})
        files = await cursor.to_list(length=None)

        # Преобразование ObjectId в строку для JSON-сериализации
        for file in files:
            file["_id"] = str(file["_id"])

        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/")
async def list_files(request: Request, user: Users = Depends(get_current_user)):
    try:
        db = request.app.mongodb
        fs = AsyncIOMotorGridFSBucket(db)
        cursor = fs.find({"metadata.user_id": user.id})
        files = await cursor.to_list(length=None)

        for file in files:
            file["_id"] = str(file["_id"])

        return files
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
