from apscheduler.schedulers.asyncio import AsyncIOScheduler
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
    except Exception as e:
        logger.error(f"Error during cleanup database: {str(e)}", exc_info=True)


def setup_scheduler():
    scheduler.add_job(
        cleanup_unverified_users, "interval", minutes=10, id="cleanup_unverified_users"
    )
    scheduler.start()
