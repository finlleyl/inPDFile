import urllib
from datetime import datetime
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from pdf2image import convert_from_bytes
from sqlalchemy.exc import SQLAlchemyError

# from app.pdf.predict import (
#     add_bboxs_on_img,
#     detect_sample_model,
#     get_bytes_from_image,
# )
from app.pdf.schemas import SHistoryOut, SUploadOut
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.pdf.models import PdfDocuments, PdfProcessingHistory
from app.database import SessionManager
from app.pdf.dao import PdfDocumentsDAO
from app.dao.mongodb_dao import MongoDBStorageDAO
from app.logger import logger


router = APIRouter(
    prefix="/pdf",
    tags=["Pdf"],
)


@router.post("/upload", response_model=SUploadOut)
async def upload_pdf(
    request: Request,
    file: UploadFile = File(...),
    user: Users = Depends(get_current_user),
):
    mongo_dao = MongoDBStorageDAO(request.app.mongodb)

    async with SessionManager() as session:
        try:
            file_id = await mongo_dao.upload_file(
                file.filename,
                file.file,
                metadata={
                    "user_id": user.id,
                    "content_type": file.content_type,
                    "timestamp": datetime.utcnow(),
                },
            )

            pdf_document = PdfDocuments(
                user_id=user.id,
                file_name=file.filename,
                file_path=file_id,
                file_size=file.size,
                upload_date=datetime.utcnow(),
                status="в очереди",
                classification="не определена",
                document_metadata={},
                document_type="не определен",
                has_signature=False,
                has_stamp=False,
            )
            session.add(pdf_document)
            await session.flush()

            history_entry = PdfProcessingHistory(
                document_id=pdf_document.id,
                status="загружен",
                timestamp=datetime.utcnow(),
                log="Файл успешно загружен в систему.",
            )
            session.add(history_entry)

            return {"file_id": file_id, "document_id": pdf_document.id, "status": "ok"}

        except SQLAlchemyError as e:
            await session.rollback()
            return {
                "file_id": "0",
                "document_id": 0,
                "status": str(e),
            }
        except (IOError, ValueError) as e:
            raise HTTPException(
                status_code=400, detail=f"Ошибка загрузки файла: {str(e)}"
            ) from e
        except Exception as e:
            logger.exception("Непредвиденная ошибка при загрузке файла")
            raise HTTPException(
                status_code=500, detail=f"Ошибка загрузки файла: {str(e)}"
            ) from e


@router.post("/analyze")
async def analyze_pdf(
    request: Request,
    file: UploadFile = File(...),
    user: Users = Depends(get_current_user),
):

    # page_number = 0
    pdf_bytes = await file.read()
    # if page_number:
    #     pages = convert_from_bytes(
    #         pdf_bytes,
    #         poppler_path="/usr/bin",
    #         dpi=300,
    #         first_page=page_number,
    #         last_page=page_number,
    #     )
    # else:
    pages = convert_from_bytes(pdf_bytes, dpi=300)

    predict = detect_sample_model(pages[0])

    final_image = add_bboxs_on_img(image=pages[0], predict=predict)

    return StreamingResponse(
        content=get_bytes_from_image(final_image), media_type="image/jpeg"
    )


# @router.get("/download/{file_id}")
# async def download_pdf(
#     file_id: str, request: Request, _user: Users = Depends(get_current_user)
# ):
#     mongo_dao = MongoDBStorageDAO(request.app.mongodb)
#     grid_out = await mongo_dao.download_file(file_id)

#     filename = grid_out.filename or "default.pdf"
#     filename_encoded = urllib.parse.quote(filename)
#     content_disposition = f"attachment; filename*=UTF-8''{filename_encoded}"

#     async def chunk_generator():
#         while True:
#             chunk = await grid_out.readchunk()
#             if not chunk:
#                 break
#             yield chunk

#     return StreamingResponse(
#         chunk_generator(),
#         media_type="application/pdf",
#         headers={"Content-Disposition": content_disposition},
#     )


@router.get("/all_files/")
async def list_all_files(request: Request, _user: Users = Depends(get_current_user)):
    mongo_dao = MongoDBStorageDAO(request.app.mongodb)
    return await mongo_dao.list_all_files()


@router.get("/files/")
async def list_files(request: Request, user: Users = Depends(get_current_user)):
    mongo_dao = MongoDBStorageDAO(request.app.mongodb)
    return await mongo_dao.list_user_files(user.id)


@router.get("/history/", response_model=list[SHistoryOut])
async def get_users_history(_request: Request, user: Users = Depends(get_current_user)):
    try:
        results = await PdfDocumentsDAO.find_all(user_id=int(user.id))
        final_history = []

        for result in results:
            new_item = {}

            new_item["file_name"] = result["file_name"]
            cur_size = int(result["file_size"]) / (1024 * 1024)
            new_item["file_size"] = f"{cur_size:.2f} MB"
            new_item["file_path"] = result["file_path"]
            new_item["status"] = result["status"]
            new_item["classification"] = result["classification"]
            new_item["document_type"] = result["document_type"]

            if isinstance(result["upload_date"], datetime):  # Проверяем тип данных
                formatted_date = result["upload_date"].strftime("%d.%m.%Y %H:%M:%S")
            else:
                date_str = str(result["upload_date"])
                date_obj = datetime.fromisoformat(date_str)
                formatted_date = date_obj.strftime("%d.%m.%Y %H:%M:%S")

            new_item["upload_date"] = formatted_date

            new_item["has_signature"] = (
                "Имеет подпись" if result["has_signature"] else "Не имеет подпись"
            )
            new_item["has_stamp"] = (
                "Имеет печать" if result["has_stamp"] else "Не имеет печать"
            )

            final_history.append(new_item)

        return final_history

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
