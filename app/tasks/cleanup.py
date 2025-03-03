from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.users.dao import UsersDAO
from app.logger import logger

scheduler = AsyncIOScheduler()


async def cleanup_unverified_users():
    try:
        count_inactive_users = await UsersDAO.delete(is_verified=False)
        msg = (
            f"Cleanup unverified users completed. Deleted {count_inactive_users} users"
        )
        logger.info(msg, extra={"count_inactive_users": count_inactive_users})
    except SQLAlchemyError as e:
        return {"error": "Ошибка при сохранении данных в БД", "details": str(e)}
    except (IOError, ValueError) as e:
        raise HTTPException(
            status_code=400, detail=f"Ошибка загрузки файла: {str(e)}"
        ) from e
    except Exception as e:
        logger.exception("Непредвиденная ошибка при загрузке файла")
        raise HTTPException(
            status_code=500, detail=f"Ошибка загрузки файла: {str(e)}"
        ) from e


def setup_scheduler():
    scheduler.add_job(
        cleanup_unverified_users, "interval", minutes=10, id="cleanup_unverified_users"
    )
    scheduler.start()
