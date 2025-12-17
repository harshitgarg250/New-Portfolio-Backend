from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceUpdate, ExperienceResponse
from app.core.security import get_current_admin_user

router = APIRouter()

@router.get("", response_model=dict)
async def get_experiences(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Experience).order_by(Experience.order, Experience.start_date.desc())
    )
    experiences = result.scalars().all()
    return {"data": experiences, "total": len(experiences)}

@router.get("/{id}", response_model=ExperienceResponse)
async def get_experience(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Experience).where(Experience.id == id))
    experience = result.scalar_one_or_none()
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    return experience

@router.post("", response_model=ExperienceResponse)
async def create_experience(
    experience_in: ExperienceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    experience = Experience(**experience_in.model_dump())
    db.add(experience)
    await db.commit()
    await db.refresh(experience)
    return experience

@router.put("/{id}", response_model=ExperienceResponse)
async def update_experience(
    id: int,
    experience_in: ExperienceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Experience).where(Experience.id == id))
    experience = result.scalar_one_or_none()
    
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    update_data = experience_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experience, field, value)
    
    await db.commit()
    await db.refresh(experience)
    return experience

@router.delete("/{id}")
async def delete_experience(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Experience).where(Experience.id == id))
    experience = result.scalar_one_or_none()
    
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    await db.delete(experience)
    await db.commit()
    
    return {"message": "Experience deleted successfully"}
