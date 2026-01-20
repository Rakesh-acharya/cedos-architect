# CEDOS - Complete Run Instructions

## 🚀 Quick Start Guide

Follow these steps to get CEDOS up and running on your system.

---

## Prerequisites

Before starting, ensure you have:

- **Python 3.9+** installed
- **PostgreSQL 12+** installed and running
- **Node.js 16+** and npm installed
- **Git** (optional, for cloning)

---

## Step 1: Database Setup

### Option A: Using PostgreSQL Command Line

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE cedos_db;
CREATE USER cedos_user WITH PASSWORD 'cedos_pass';
GRANT ALL PRIVILEGES ON DATABASE cedos_db TO cedos_user;
\q
```

### Option B: Using createdb (if available)

```bash
createdb -U postgres cedos_db
```

---

## Step 2: Backend Setup

### 2.1 Navigate to Backend Directory

```bash
cd backend
```

### 2.2 Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2.4 Configure Environment

Create a `.env` file in the `backend` directory:

```bash
# Copy example file
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
DATABASE_URL=postgresql://cedos_user:cedos_pass@localhost/cedos_db
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=10080
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

### 2.5 Run Database Migrations

```bash
# Initialize Alembic (if not already done)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 2.6 Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:**
- API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

---

## Step 3: Frontend Setup

### 3.1 Navigate to Frontend Directory

Open a **new terminal window** and:

```bash
cd frontend
```

### 3.2 Install Dependencies

```bash
npm install
```

### 3.3 Start Frontend Development Server

```bash
npm run dev
```

**Frontend will be available at:**
- http://localhost:3000

---

## Step 4: Create Admin User

### Option A: Using API (Recommended)

Open a new terminal or use Postman/curl:

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

### Option B: Using Python Script

Create a file `create_admin.py` in backend directory:

```python
from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

db = SessionLocal()

admin = User(
    email="admin@cedos.com",
    username="admin",
    full_name="System Administrator",
    role=UserRole.ADMIN,
    hashed_password=get_password_hash("admin123"),
    is_active=True,
    is_verified=True
)

db.add(admin)
db.commit()
print("Admin user created successfully!")
```

Run it:
```bash
python create_admin.py
```

---

## Step 5: Login and Test

### 5.1 Login via API

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Save the `access_token` from the response.

### 5.2 Test API Endpoint

```bash
# Replace YOUR_TOKEN with the access token from login
curl -X GET "http://localhost:8000/api/v1/projects/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 5.3 Login via Frontend

1. Open http://localhost:3000
2. Click "Login"
3. Enter:
   - Username: `admin`
   - Password: `admin123`

---

## Step 6: Create Your First Project

### Via Frontend:
1. Navigate to Projects
2. Click "Create New Project"
3. Fill in project details
4. Submit

### Via API:

```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "My First Building",
    "project_type": "residential_building",
    "location": "Mumbai",
    "usage_type": "residential",
    "seismic_zone": "Zone III",
    "soil_bearing_capacity": 200,
    "design_life_years": 50
  }'
```

---

## Step 7: Perform Calculations

### Example: Column Design

```bash
curl -X POST "http://localhost:8000/api/v1/calculations/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
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

### Example: Road Design

```bash
curl -X POST "http://localhost:8000/api/v1/calculations/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "calculation_type": "road_design",
    "input_parameters": {
      "traffic_count": 5000,
      "design_life": 20,
      "subgrade_cbr": 5.0,
      "pavement_type": "flexible",
      "design_speed": 80,
      "road_class": "NH"
    }
  }'
```

---

## Step 8: Generate BOQ

```bash
curl -X POST "http://localhost:8000/api/v1/boq/generate/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Step 9: Generate Cost Estimate

```bash
curl -X POST "http://localhost:8000/api/v1/cost/estimate/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Step 10: Download PDFs

### Calculation Sheet:
```bash
curl -X GET "http://localhost:8000/api/v1/documents/download/calculation/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output calculation.pdf
```

### BOQ:
```bash
curl -X GET "http://localhost:8000/api/v1/documents/download/boq/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output boq.pdf
```

### Blueprint (Plan View):
```bash
curl -X GET "http://localhost:8000/api/v1/blueprints/plan/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output plan.pdf
```

---

## Step 11: AR Visualization (Mobile)

### 11.1 Generate AR Data

```bash
curl -X POST "http://localhost:8000/api/v1/ar/generate/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "site_length": 10,
    "site_width": 10,
    "site_height": 5
  }'
```

### 11.2 Access AR View on Mobile

1. Ensure backend is accessible from your mobile device (same network or public IP)
2. Open mobile browser: `http://YOUR_IP:3000/ar/1`
3. Allow camera access
4. Point camera at site markers
5. Blueprint will overlay on real-world view

---

## Running Tests

```bash
cd backend
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_calculations.py
pytest tests/test_road_bridge_drainage.py
```

---

## Troubleshooting

### Database Connection Error

**Problem:** `psycopg2.OperationalError: could not connect to server`

**Solutions:**
1. Check PostgreSQL is running: `sudo systemctl status postgresql` (Linux) or check Services (Windows)
2. Verify database credentials in `.env`
3. Check PostgreSQL port (default: 5432)

### Migration Errors

**Problem:** `alembic.util.exc.CommandError: Target database is not up to date`

**Solutions:**
```bash
# Check current revision
alembic current

# Upgrade to head
alembic upgrade head

# If issues persist, reset (WARNING: deletes data)
alembic downgrade base
alembic upgrade head
```

### Port Already in Use

**Problem:** `Address already in use`

**Solutions:**
1. Change port in `uvicorn` command: `--port 8001`
2. Kill process using port:
   - Windows: `netstat -ano | findstr :8000` then `taskkill /PID <PID> /F`
   - Linux/Mac: `lsof -ti:8000 | xargs kill`

### Frontend Build Errors

**Problem:** `npm install` fails

**Solutions:**
```bash
# Clear cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors

**Problem:** Frontend can't connect to backend

**Solutions:**
1. Check `BACKEND_CORS_ORIGINS` in `.env` includes frontend URL
2. Ensure backend is running
3. Check browser console for specific error

---

## Production Deployment

### Backend (Using Gunicorn)

```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000
```

### Frontend (Build)

```bash
cd frontend
npm run build
# Serve dist/ folder with nginx or similar
```

### Environment Variables for Production

Update `.env`:
```env
SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-database-url>
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

---

## Key Features to Test

1. ✅ **Project Creation** - Create projects with different types
2. ✅ **Calculations** - Test all calculation types (buildings, roads, bridges, drainage)
3. ✅ **BOQ Generation** - Generate BOQ from calculations
4. ✅ **Cost Estimation** - Create cost estimates
5. ✅ **Compliance Checking** - Verify compliance validation
6. ✅ **PDF Downloads** - Download calculation sheets, BOQ, cost estimates
7. ✅ **Blueprint Generation** - Generate plan, elevation, section views
8. ✅ **AR Visualization** - Test AR on mobile device
9. ✅ **Audit Logging** - Check audit trail for actions

---

## API Documentation

Once backend is running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## Support

For issues or questions:
1. Check [SETUP.md](SETUP.md) for detailed setup
2. Review [ARCHITECTURE.md](ARCHITECTURE.md) for system details
3. See [FEATURES.md](FEATURES.md) for feature list

---

## Next Steps

1. Explore all calculation types
2. Generate blueprints for your designs
3. Test AR visualization on mobile
4. Create comprehensive projects
5. Export all documents as PDFs
6. Review audit logs

**Happy Engineering! 🏗️**
