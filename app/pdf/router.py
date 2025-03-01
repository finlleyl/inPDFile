from datetime import datetime
from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from app.exceptions import FileNotPDFException
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from fastapi.responses import StreamingResponse
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.logger import logger
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
    # if file.content_type != "application/pdf":
    # raise FileNotPDFException

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


@router.get("/download/{file_id}")
async def download_pdf(
    file_id: str, request: Request, user: Users = Depends(get_current_user)
):
    fs = AsyncIOMotorGridFSBucket(request.app.mongodb)

    try:
        file_id = ObjectId(file_id)
        grid_out = await fs.open_download_stream(file_id)

        # Получаем имя файла
        filename = grid_out.filename or "default.pdf"
        filename_encoded = urllib.parse.quote(filename)
        content_disposition = f"attachment; filename*=UTF-8''{filename_encoded}"

        # Генератор для потоковой передачи
        async def chunk_generator():
            while True:
                chunk = await grid_out.readchunk()
                if not chunk:
                    break
                yield chunk

        return StreamingResponse(
            chunk_generator(),
            media_type="application/pdf",
            headers={"Content-Disposition": content_disposition},
        )

    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=404, detail="File not found")


@router.get("/all_files/")
async def list_files(request: Request, user: Users = Depends(get_current_user)):
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
