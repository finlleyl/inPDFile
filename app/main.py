import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from prometheus_fastapi_instrumentator import Instrumentator
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from app.tasks.cleanup import scheduler
from app.users.router import router as router_users
from app.pdf.router import router as router_pdf
from app.logger import logger
from app.config import settings
from app.tasks.cleanup import setup_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):

    startup_time = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Application startup", extra={"startup_time": startup_time})
    setup_scheduler()
    try:
        app.mongodb_client = AsyncIOMotorClient(
            settings.mongodb_url,
            maxPoolSize=100,
            minPoolSize=10,
        )
        app.mongodb = app.mongodb_client[settings.MONGO_INITDB_DB_NAME]
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"MongoDB connection error: {str(e)}", exc_info=True)
        raise

    yield

    app.mongodb_client.close()
    scheduler.shutdown()
    shutdown_time = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Application shutdown", extra={"shutdown_time": shutdown_time})


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)
app.include_router(router_pdf)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_respect_env_var=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    inprogress_name="inprogress",
    inprogress_labels=True,
)

Instrumentator().instrument(app).expose(app)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(
        "Request execution time", extra={"process_time": round(process_time, 4)}
    )
    return response
