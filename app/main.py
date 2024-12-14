from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# @asynccontextmanager
# async def lifespan(_: FastAPI) -> AsyncIterator[None]:
#     redis = aioredis.from_url("redis://localhost:6379")
#     FastAPICache.init(RedisBackend(redis), prefix="cache")
#     yield

app = FastAPI(lifespan=lifespan)

# app.mount("/static", StaticFiles(directory="app/static"), name="static")

# app.include_router(router_users)


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

