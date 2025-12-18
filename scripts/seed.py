import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import engine, AsyncSessionLocal, Base
from app.models.project import Project
from app.models.post import Post
from app.models.skill import Skill
from app.models.testimonial import Testimonial
from app.models.service import Service


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def seed():
    async with AsyncSessionLocal() as session:  # type: AsyncSession
        # Projects
        projects = [
            Project(
                title="Demo Portfolio Site",
                slug="demo-portfolio",
                description="A demo portfolio site powered by the CMS",
                content="Detailed content for demo portfolio",
                category="Web App",
                technologies=["React", "FastAPI", "Tailwind"],
                github_url="#",
                live_url="#",
                year="2025",
                is_featured=True,
            ),
            Project(
                title="API Service",
                slug="api-service",
                description="Headless API for content",
                content="API details",
                category="API",
                technologies=["FastAPI", "Postgres"],
            ),
        ]

        # Posts
        posts = [
            Post(
                title="Getting Started with the CMS",
                slug="getting-started-cms",
                excerpt="Intro to the custom CMS",
                content="This post explains how to use the CMS",
            ),
        ]

        # Skills
        skills = [
            Skill(name="Python", category="Language", level="Expert", proficiency=95),
            Skill(name="JavaScript", category="Language", level="Advanced", proficiency=85),
        ]

        # Testimonials
        testimonials = [
            Testimonial(author="Jane Doe", role="Client", content="Great work!", featured=True),
        ]

        # Services
        services = [
            Service(title="Web Development", subtitle="Full-stack apps", description="Build modern web apps."),
            Service(title="API Development", subtitle="Robust APIs", description="Design and build APIs."),
        ]

        session.add_all(projects + posts + skills + testimonials + services)
        await session.commit()


async def main():
    print("Creating tables...")
    await create_tables()
    print("Seeding data...")
    await seed()
    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
