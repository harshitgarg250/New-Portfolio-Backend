# Portfolio Backend API

FastAPI backend for portfolio website and CMS.

## Features

- 🔐 JWT Authentication
- 👤 User profile management
- 💼 Projects API
- 📝 Blog posts API
- 🛠️ Skills API
- 📅 Experience API
- 📬 Contact form API
- 📁 File upload handling

## Tech Stack

- FastAPI 0.104
- SQLAlchemy 2.0 (async)
- PostgreSQL with asyncpg
- Alembic (migrations)
- Pydantic 2.5
- python-jose (JWT)
- bcrypt (password hashing)

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload
```

## Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/portfolio
SECRET_KEY=your-super-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
UPLOAD_DIR=uploads
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### Profile
- `GET /api/profile` - Get profile
- `PUT /api/profile` - Update profile

### Projects
- `GET /api/projects` - List projects
- `GET /api/projects/{id}` - Get project
- `POST /api/projects` - Create project
- `PUT /api/projects/{id}` - Update project
- `DELETE /api/projects/{id}` - Delete project

### Posts
- `GET /api/posts` - List posts
- `GET /api/posts/{slug}` - Get post by slug
- `POST /api/posts` - Create post
- `PUT /api/posts/{id}` - Update post
- `DELETE /api/posts/{id}` - Delete post

### Skills
- `GET /api/skills` - List skills
- `POST /api/skills` - Create skill
- `PUT /api/skills/{id}` - Update skill
- `DELETE /api/skills/{id}` - Delete skill

### Experience
- `GET /api/experience` - List experience
- `POST /api/experience` - Create experience
- `PUT /api/experience/{id}` - Update experience
- `DELETE /api/experience/{id}` - Delete experience

### Contact
- `GET /api/contact` - List messages (auth required)
- `POST /api/contact` - Submit message
- `PUT /api/contact/{id}` - Update message
- `DELETE /api/contact/{id}` - Delete message

### Upload
- `POST /api/upload` - Upload file

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── profile.py
│   │   ├── projects.py
│   │   ├── posts.py
│   │   ├── skills.py
│   │   ├── experience.py
│   │   ├── contact.py
│   │   ├── upload.py
│   │   └── router.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── database.py
│   ├── models/
│   │   └── *.py
│   └── schemas/
│       └── *.py
├── main.py
├── requirements.txt
└── alembic.ini
```

## Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```
