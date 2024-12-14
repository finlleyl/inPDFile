from datetime import date
from fastapi import APIRouter, Depends
from pydantic import TypeAdapter, parse_obj_as
from app.exceptions import RoomsNotbookedException
from app.tasks.tasks import send_booking_confirmation_email, train_model
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Pdf"],
)

