from pydantic import BaseModel, EmailStr
from typing import Optional, Dict
from datetime import datetime

class ProfileBase(BaseModel):
    name: str
    title: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    resume_url: Optional[str] = None
    social_links: Optional[Dict[str, str]] = {}

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    resume_url: Optional[str] = None
    social_links: Optional[Dict[str, str]] = None

class ProfileResponse(ProfileBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
