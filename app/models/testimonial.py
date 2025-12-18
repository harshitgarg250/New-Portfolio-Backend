from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.sql import func
from app.db.database import Base


class Testimonial(Base):
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(String(128), nullable=False)
    role = Column(String(128), nullable=True)
    content = Column(Text, nullable=False)
    featured = Column(Boolean, default=False)
