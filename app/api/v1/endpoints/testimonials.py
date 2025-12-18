from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.models.testimonial import Testimonial
from app.schemas.testimonial import (
    TestimonialCreate,
    TestimonialUpdate,
    TestimonialOut,
)

router = APIRouter()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@router.get("", response_model=List[TestimonialOut])
async def list_testimonials(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Testimonial))
    items = result.scalars().all()
    return items


@router.post("", response_model=TestimonialOut, status_code=status.HTTP_201_CREATED)
async def create_testimonial(data: TestimonialCreate, db: AsyncSession = Depends(get_db)):
    obj = Testimonial(**data.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/{item_id}", response_model=TestimonialOut)
async def get_testimonial(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Testimonial).where(Testimonial.id == item_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return obj


@router.put("/{item_id}", response_model=TestimonialOut)
async def update_testimonial(item_id: int, data: TestimonialUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Testimonial).where(Testimonial.id == item_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_testimonial(item_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Testimonial).where(Testimonial.id == item_id))
    obj = result.scalar_one_or_none()
    if obj is None:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    await db.delete(obj)
    await db.commit()
    return None
