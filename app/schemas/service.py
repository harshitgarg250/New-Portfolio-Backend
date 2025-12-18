from pydantic import BaseModel
from typing import Optional


class ServiceBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(ServiceBase):
    pass


class ServiceOut(ServiceBase):
    id: int

    class Config:
        orm_mode = True
