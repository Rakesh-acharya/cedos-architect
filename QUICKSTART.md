# CEDOS Quick Start Guide

## Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Node.js 16+ (for frontend)
- Git

## 5-Minute Setup

### 1. Clone and Setup Backend

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials
```

### 2. Setup Database

```bash
# Create PostgreSQL database
createdb cedos_db

# Or using psql:
psql -U postgres
CREATE DATABASE cedos_db;
CREATE USER cedos_user WITH PASSWORD 'cedos_pass';
GRANT ALL PRIVILEGES ON DATABASE cedos_db TO cedos_user;
\q
```

### 3. Run Migrations

```bash
cd backend
alembic upgrade head
```

### 4. Start Backend Server

```bash
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API docs at: http://localhost:8000/api/docs

### 5. Create Admin User

Using the API:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@cedos.com",
    "username": "admin",
    "full_name": "System Administrator",
    "role": "admin",
    "password": "admin123"
  }'
```

### 6. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Save the `access_token` from the response.

### 7. Create Your First Project

```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "My First Project",
    "project_type": "residential_building",
    "location": "Mumbai",
    "usage_type": "residential",
    "seismic_zone": "Zone III",
    "soil_bearing_capacity": 200
  }'
```

### 8. Perform a Calculation

```bash
curl -X POST "http://localhost:8000/api/v1/calculations/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "calculation_type": "column_design",
    "input_parameters": {
      "axial_load": 2000,
      "concrete_grade": "M25",
      "steel_grade": "Fe415"
    }
  }'
```

### 9. Generate BOQ

```bash
curl -X POST "http://localhost:8000/api/v1/boq/generate/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 10. Generate Cost Estimate

```bash
curl -X POST "http://localhost:8000/api/v1/cost/estimate/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Frontend Setup (Optional)

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:3000

## Next Steps

1. Explore API documentation at http://localhost:8000/api/docs
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) for system details
3. Check [FEATURES.md](FEATURES.md) for feature list
4. Review [SETUP.md](SETUP.md) for detailed setup

## Common Issues

### Database Connection Error
- Check PostgreSQL is running
- Verify credentials in `.env`
- Ensure database exists

### Migration Errors
- Make sure database is empty or use `alembic upgrade head`
- Check database user has proper permissions

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Support

For detailed documentation, see:
- [SETUP.md](SETUP.md) - Full setup guide
- [ARCHITECTURE.md](ARCHITECTURE.md) - System architecture
- [FEATURES.md](FEATURES.md) - Feature documentation
