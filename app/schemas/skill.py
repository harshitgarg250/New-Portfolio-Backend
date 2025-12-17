from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    level: Optional[str] = None
    proficiency: int = 0
    is_active: bool = True
    order: int = 0

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    level: Optional[str] = None
    proficiency: Optional[int] = None
    is_active: Optional[bool] = None
    order: Optional[int] = None

class SkillResponse(SkillBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
