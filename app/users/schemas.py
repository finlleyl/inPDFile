from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class SUser(BaseModel):
    id: int
    email: str
    hashed_password: str
    is_verified: bool
    registration_date: datetime
    last_login_date: datetime
    is_active: bool
    is_superuser: bool


class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=20)


class SUserAuthOut(BaseModel):
    message: str
    access_token: str
    user_id: int


class SUserConfirm(BaseModel):
    code: int


class SUserConfirmOut(BaseModel):
    message: str
    user_id: int


class SUserDelete(BaseModel):
    message: str
    user_id: int
