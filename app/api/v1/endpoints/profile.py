from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.core.security import get_current_admin_user

router = APIRouter()

@router.get("", response_model=ProfileResponse)
async def get_profile(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Profile).limit(1))
    profile = result.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("", response_model=ProfileResponse)
async def create_profile(
    profile_in: ProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    # Check if profile exists
    result = await db.execute(select(Profile).limit(1))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    profile = Profile(**profile_in.model_dump())
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile

@router.put("", response_model=ProfileResponse)
async def update_profile(
    profile_in: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Profile).limit(1))
    profile = result.scalar_one_or_none()
    
    if not profile:
        # Create if not exists
        profile = Profile(**profile_in.model_dump(exclude_unset=True))
        db.add(profile)
    else:
        # Update existing
        update_data = profile_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    return profile
