from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from app.db.database import get_db
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate, ContactResponse
from app.core.security import get_current_admin_user

router = APIRouter()

@router.post("", response_model=ContactResponse)
async def create_contact(
    contact_in: ContactCreate,
    db: AsyncSession = Depends(get_db)
):
    """Public endpoint to submit contact form"""
    contact = Contact(**contact_in.model_dump())
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

@router.get("", response_model=dict)
async def get_contacts(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    """Admin endpoint to get all contacts"""
    result = await db.execute(
        select(Contact).order_by(desc(Contact.created_at))
    )
    contacts = result.scalars().all()
    
    # Count unread
    unread_result = await db.execute(
        select(Contact).where(Contact.is_read == False)
    )
    unread_count = len(unread_result.scalars().all())
    
    return {"data": contacts, "total": len(contacts), "unread": unread_count}

@router.get("/{id}", response_model=ContactResponse)
async def get_contact(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Contact).where(Contact.id == id))
    contact = result.scalar_one_or_none()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.put("/{id}", response_model=ContactResponse)
async def update_contact(
    id: int,
    contact_in: ContactUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Contact).where(Contact.id == id))
    contact = result.scalar_one_or_none()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_data = contact_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(contact, field, value)
    
    await db.commit()
    await db.refresh(contact)
    return contact

@router.delete("/{id}")
async def delete_contact(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_admin_user)
):
    result = await db.execute(select(Contact).where(Contact.id == id))
    contact = result.scalar_one_or_none()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    await db.delete(contact)
    await db.commit()
    
    return {"message": "Contact deleted successfully"}
