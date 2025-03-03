from fastapi import APIRouter
from fastapi.templating import Jinja2Templates



router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"],
)

templates = Jinja2Templates(directory="app/templates")

