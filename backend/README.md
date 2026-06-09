# SkillBridge Backend (Phase 1)

This repo already has the FastAPI scaffold + SQLAlchemy models. Phase 1 completion adds:
- Initial Alembic migration
- Local storage placeholders
- Seed data script

## Prerequisites

Choose one:

### Option A (recommended): Docker Desktop
- Install Docker Desktop for Windows and make sure the Docker engine is running.

### Option B: Local services
- PostgreSQL 16 running locally
- (Optional) Redis + Qdrant

## Environment

From `backend/`:

1. Create `.env` from `.env.example`.
2. Ensure `DATABASE_URL` points to your Postgres instance.

For Docker Compose networking, use:
- `postgresql+asyncpg://skillbridge:skillbridge_dev@postgres:5432/skillbridge`

For local Postgres, use:
- `postgresql+asyncpg://skillbridge:skillbridge_dev@localhost:5432/skillbridge`

## Install Python deps (Phase 1 only)

From `backend/`:

- `python -m pip install -r requirements.phase1.txt`

(Full Phase 3+ AI deps are in `requirements.txt`, but they can require Python 3.12 wheels.)

## Start services

From repo root:

- `docker compose up -d postgres redis qdrant`

If Docker is not available, start Postgres locally and skip the other two.

## Run migrations

From `backend/`:

- `python -m alembic upgrade head`

The initial migration is in `alembic/versions/0001_init_schema.py`.

## Seed data

From `backend/`:

- `python scripts/seed_data.py --truncate-first --students 1000 --jobs 500 --internships 500 --mentors 100 --courses 300`

## Run the API

From `backend/`:

- `uvicorn app.main:app --reload`

API health:
- `GET http://localhost:8000/health`
