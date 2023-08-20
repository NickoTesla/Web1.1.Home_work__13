from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    avatar: str

    class Config:
        from_attributes = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ContactBase(BaseModel):
    first_name: str = Field(..., max_length=50, description="First name of the contact")
    last_name: str = Field(..., max_length=50, description="Last name of the contact")
    email: EmailStr = Field(..., description="Email address of the contact")
    phone_number: str = Field(..., max_length=20, description="Phone number of the contact")
    birth_date: Optional[date] = Field(None, description="Birth date of the contact (YYYY-MM-DD)")
    additional_data: Optional[str] = Field(None, description="Additional data about the contact")

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int 
    created_at: datetime | None 
    updated_at: datetime | None
    user: UserResponse | None


    class Config:
        from_attributes = True


# added

class RequestEmail(BaseModel):
    email: EmailStr