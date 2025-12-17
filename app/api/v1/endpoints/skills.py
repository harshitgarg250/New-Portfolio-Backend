from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.database import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate, SkillResponse
from app.core.security import get_current_admin_user

router = APIRouter()

@router.get("", response_model=dict)
async def get_skills(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Skill).where(Skill.is_active == True).order_by(Skill.order, Skill.name)
    )
    skills = result.scalars().all()
    return {"data": skills, "total": len(skills)}

@router.get("/{id}", response_model=SkillResponse)
async def get_skill(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Skill).where(Skill.id == id))
    skill = result.scalar_one_or_none()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.post("", response_model=SkillResponse)
async def create_skill(
    skill_in: SkillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    skill = Skill(**skill_in.model_dump())
    db.add(skill)
    await db.commit()
    await db.refresh(skill)
    return skill

@router.put("/{id}", response_model=SkillResponse)
async def update_skill(
    id: int,
    skill_in: SkillUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Skill).where(Skill.id == id))
    skill = result.scalar_one_or_none()
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    update_data = skill_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(skill, field, value)
    
    await db.commit()
    await db.refresh(skill)
    return skill

@router.delete("/{id}")
async def delete_skill(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Skill).where(Skill.id == id))
    skill = result.scalar_one_or_none()
    
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    await db.delete(skill)
    await db.commit()
    
    return {"message": "Skill deleted successfully"}
