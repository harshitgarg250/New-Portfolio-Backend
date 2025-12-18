from sqlalchemy import Column, Integer, String, Text, Boolean
from app.db.database import Base


class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(128), nullable=False)
    subtitle = Column(String(256), nullable=True)
    description = Column(Text, nullable=True)
    active = Column(Boolean, default=True)
