# Database Reset & Migration Guide

## Quick Fix for "type already exists" Error

Run these commands in order:

### 1. Activate Virtual Environment
```cmd
.venv\Scripts\activate
```

### 2. Reset Database (Drop Everything)
```cmd
python reset_db.py
```

### 3. Run Migration Again
```cmd
python -m alembic upgrade head
```

### 4. Seed Data
```cmd
python scripts/seed_data.py --truncate-first --students 1000 --jobs 500 --internships 500 --mentors 100 --courses 300
```

## Alternative: Manual SQL Reset

If the script doesn't work, connect to PostgreSQL and run:

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Using psql:
```cmd
docker exec -it skillbridge-postgres psql -U skillbridge -d skillbridge -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

## Verify Database is Clean

```cmd
python -m alembic current
```

Should show: "None" (no migrations applied)
