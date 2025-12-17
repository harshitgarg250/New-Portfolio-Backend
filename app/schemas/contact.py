from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactBase(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

class ContactCreate(ContactBase):
    pass

class ContactUpdate(BaseModel):
    is_read: Optional[bool] = None

class ContactResponse(ContactBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
