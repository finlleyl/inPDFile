from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates



router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")

