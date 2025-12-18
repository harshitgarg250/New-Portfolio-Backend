from fastapi import APIRouter

from app.api.v1.endpoints import (
	auth,
	profile,
	projects,
	posts,
	skills,
	experience,
	contact,
	upload,
	testimonials,
	services,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_router.include_router(projects.router, prefix="/projects", tags=["Projects"])
api_router.include_router(posts.router, prefix="/posts", tags=["Blog Posts"])
api_router.include_router(skills.router, prefix="/skills", tags=["Skills"])
api_router.include_router(experience.router, prefix="/experience", tags=["Experience"])
api_router.include_router(contact.router, prefix="/contact", tags=["Contact"])
api_router.include_router(upload.router, prefix="/upload", tags=["Upload"])
api_router.include_router(testimonials.router, prefix="/testimonials", tags=["Testimonials"])
api_router.include_router(services.router, prefix="/services", tags=["Services"])
