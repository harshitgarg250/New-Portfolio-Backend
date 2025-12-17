from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ExperienceBase(BaseModel):
    title: str
    organization: str
    type: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = []
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    order: int = 0

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    type: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: Optional[bool] = None
    order: Optional[int] = None

class ExperienceResponse(ExperienceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
