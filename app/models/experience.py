from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON
from sqlalchemy.sql import func
from app.db.database import Base

class Experience(Base):
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False)
    type = Column(String(50))  # Work, Education, Certification
    location = Column(String(255))
    description = Column(Text)
    skills = Column(JSON, default=[])
    start_date = Column(String(50))
    end_date = Column(String(50))  # null means current
    is_current = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
