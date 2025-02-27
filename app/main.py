import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import router as router_users
from app.logger import logger
from app.tasks.cleanup import scheduler, setup_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
   
    startup_time = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Application startup", extra={"startup_time": startup_time})
    setup_scheduler()  
    yield
    
    scheduler.shutdown()  
    shutdown_time = time.strftime("%Y-%m-%d %H:%M:%S")
    logger.info("Application shutdown", extra={"shutdown_time": shutdown_time})


app = FastAPI(lifespan=lifespan)

app.include_router(router_users)


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


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
