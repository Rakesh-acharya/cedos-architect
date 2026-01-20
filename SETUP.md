# CEDOS Setup Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Node.js 16+ (for frontend)
- npm or yarn

## Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Setup PostgreSQL database**
```bash
# Create database
createdb cedos_db

# Or using psql:
psql -U postgres
CREATE DATABASE cedos_db;
CREATE USER cedos_user WITH PASSWORD 'cedos_pass';
GRANT ALL PRIVILEGES ON DATABASE cedos_db TO cedos_user;
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials and secret key
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start backend server**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/api/docs

## Frontend Setup (Coming Soon)

```bash
cd frontend
npm install
npm start
```

## Initial Data Setup

After starting the backend, create an admin user:

```bash
# Use the API endpoint
POST /api/v1/auth/register
{
  "email": "admin@cedos.com",
  "username": "admin",
  "full_name": "System Administrator",
  "role": "admin",
  "password": "secure_password"
}
```

## Testing

Run tests:
```bash
pytest tests/
```

## Project Structure

```
cedos/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   ├── alembic/          # Database migrations
│   └── tests/             # Unit tests
└── frontend/              # React frontend (to be built)
```

## Key Features Implemented

✅ Project Management
✅ User Authentication & Authorization
✅ Structural Design Calculations
✅ Material Recommendations
✅ BOQ Generation
✅ Cost Estimation
✅ Compliance Checking
✅ Document Generation
✅ Audit Logging
✅ Progress Tracking

## Next Steps

1. Build React frontend
2. Add more engineering calculations
3. Enhance AI assistance
4. Add more code standards
5. Implement advanced reporting
