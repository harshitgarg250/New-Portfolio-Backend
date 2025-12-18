from pydantic import BaseModel
from typing import Optional


class TestimonialBase(BaseModel):
    author: str
    role: Optional[str] = None
    content: str
    featured: Optional[bool] = False


class TestimonialCreate(TestimonialBase):
    pass


class TestimonialUpdate(TestimonialBase):
    pass


class TestimonialOut(TestimonialBase):
    id: int

    class Config:
        orm_mode = True
