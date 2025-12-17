from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    technologies: Optional[List[str]] = []
    features: Optional[List[str]] = []
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    year: Optional[str] = None
    is_featured: bool = False
    is_published: bool = True
    order: int = 0

class ProjectCreate(ProjectBase):
    slug: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    category: Optional[str] = None
    technologies: Optional[List[str]] = None
    features: Optional[List[str]] = None
    github_url: Optional[str] = None
    live_url: Optional[str] = None
    year: Optional[str] = None
    is_featured: Optional[bool] = None
    is_published: Optional[bool] = None
    order: Optional[int] = None

class ProjectResponse(ProjectBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
