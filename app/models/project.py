from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, index=True, nullable=False)
    description = Column(Text)
    content = Column(Text)
    image = Column(String(500))
    category = Column(String(100))
    technologies = Column(JSON, default=[])
    features = Column(JSON, default=[])
    github_url = Column(String(500))
    live_url = Column(String(500))
    year = Column(String(10))
    is_featured = Column(Boolean, default=False)
    is_published = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
