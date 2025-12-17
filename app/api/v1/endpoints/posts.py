from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from slugify import slugify

from app.db.database import get_db
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.core.security import get_current_admin_user

router = APIRouter()

@router.get("", response_model=dict)
async def get_posts(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
):
    query = select(Post).where(Post.is_published == True)
    
    if category:
        query = query.where(Post.category == category)
    
    query = query.order_by(desc(Post.created_at)).offset(skip).limit(limit)
    
    result = await db.execute(query)
    posts = result.scalars().all()
    
    # Get total count
    count_query = select(Post).where(Post.is_published == True)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    return {"data": posts, "total": total}

@router.get("/{slug}", response_model=PostResponse)
async def get_post(slug: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post).where(Post.slug == slug, Post.is_published == True)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Increment views
    post.views += 1
    await db.commit()
    await db.refresh(post)
    
    return post

@router.post("", response_model=PostResponse)
async def create_post(
    post_in: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    # Generate slug if not provided
    slug = post_in.slug or slugify(post_in.title)
    
    # Check if slug exists
    result = await db.execute(select(Post).where(Post.slug == slug))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Post with this slug already exists")
    
    post_data = post_in.model_dump()
    post_data["slug"] = slug
    
    post = Post(**post_data)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    return post

@router.put("/{id}", response_model=PostResponse)
async def update_post(
    id: int,
    post_in: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_in.model_dump(exclude_unset=True)
    
    # Update slug if title changed
    if "title" in update_data and "slug" not in update_data:
        update_data["slug"] = slugify(update_data["title"])
    
    for field, value in update_data.items():
        setattr(post, field, value)
    
    await db.commit()
    await db.refresh(post)
    return post

@router.delete("/{id}")
async def delete_post(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Post).where(Post.id == id))
    post = result.scalar_one_or_none()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    await db.delete(post)
    await db.commit()
    
    return {"message": "Post deleted successfully"}
