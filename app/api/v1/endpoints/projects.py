from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from slugify import slugify

from app.db.database import get_db
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.core.security import get_current_admin_user

router = APIRouter()

@router.get("", response_model=dict)
async def get_projects(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    featured: Optional[bool] = None,
    category: Optional[str] = None,
):
    query = select(Project).where(Project.is_published == True)
    
    if featured is not None:
        query = query.where(Project.is_featured == featured)
    if category:
        query = query.where(Project.category == category)
    
    query = query.order_by(Project.order, desc(Project.created_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    projects = result.scalars().all()
    
    # Get total count
    count_query = select(Project).where(Project.is_published == True)
    if featured is not None:
        count_query = count_query.where(Project.is_featured == featured)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    return {"data": projects, "total": total}

@router.get("/{slug}", response_model=ProjectResponse)
async def get_project(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Project).where(Project.slug == slug, Project.is_published == True)
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("", response_model=ProjectResponse)
async def create_project(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    # Generate slug if not provided
    slug = project_in.slug or slugify(project_in.title)
    
    # Check if slug exists
    result = await db.execute(select(Project).where(Project.slug == slug))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Project with this slug already exists")
    
    project_data = project_in.model_dump()
    project_data["slug"] = slug
    
    project = Project(**project_data)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.put("/{id}", response_model=ProjectResponse)
async def update_project(
    id: int,
    project_in: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Project).where(Project.id == id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    update_data = project_in.model_dump(exclude_unset=True)
    
    # Update slug if title changed
    if "title" in update_data and "slug" not in update_data:
        update_data["slug"] = slugify(update_data["title"])
    
    for field, value in update_data.items():
        setattr(project, field, value)
    
    await db.commit()
    await db.refresh(project)
    return project

@router.delete("/{id}")
async def delete_project(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Project).where(Project.id == id))
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    await db.delete(project)
    await db.commit()
    
    return {"message": "Project deleted successfully"}
