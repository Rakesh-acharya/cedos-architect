# 🚀 CEDOS - Complete Testing & Setup Guide

## 🎯 **For Beginners - Step by Step**

This guide will help you:
1. Set up the database connection
2. Install all dependencies
3. Run comprehensive tests
4. Verify all calculations are correct
5. Start the server

---

## 📋 **Step 1: Setup Environment**

### **1.1 Install Python Dependencies**

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install all packages
pip install -r requirements.txt
pip install pytest pytest-cov requests
```

### **1.2 Setup Database Connection**

Create `.env` file in `backend/` folder:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
SECRET_KEY=cedos-secret-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**Important:** Replace `[YOUR-PASSWORD]` with your actual Supabase password.

---

## 📊 **Step 2: Database Migration**

```bash
cd backend

# Run migrations
alembic upgrade head
```

This creates all database tables.

---

## 🧪 **Step 3: Run Comprehensive Tests**

### **3.1 Run Test Suite**

```bash
cd backend
python test_and_run.py
```

**Expected Output:**
```
============================================================
CEDOS - Comprehensive Test Suite
============================================================
============================================================
Testing Database Connection...
============================================================
[OK] Database connected: db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres

============================================================
Testing Engineering Calculations...
============================================================

1. Load Calculations:
   [OK] Dead load calculation: PASSED
   [OK] Live load calculation: PASSED

2. Structural Design:
   [OK] Footing design: PASSED
   [OK] Column design: PASSED
   [OK] Beam design: PASSED

3. Road Design:
   [OK] Flexible pavement design: PASSED

4. Bridge Design:
   [OK] Bridge girder design: PASSED

5. Drainage Design:
   [OK] Storm drain design: PASSED

6. Geotechnical Analysis:
   [OK] Bearing capacity: PASSED

7. Hydrology:
   [OK] Runoff calculation: PASSED

============================================================
Test Results: 9 PASSED, 0 FAILED
============================================================
```

### **3.2 Run Pytest**

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_calculations.py -v

# With coverage report
pytest tests/ --cov=app --cov-report=html
```

---

## ✅ **Step 4: Validate Calculations**

The test suite automatically validates:
1. ✅ **Code Compliance** - All designs follow IS/IRC standards
2. ✅ **Safety Factors** - Correct factors of safety
3. ✅ **Boundary Conditions** - Edge cases handled
4. ✅ **Accuracy** - Results match expected values

### **Manual Validation Examples:**

#### **Column Design:**
- Input: 2000 kN load, M25, Fe415
- Expected: Size >= 230mm, Steel 1-4%
- **Result:** ✅ PASSES

#### **Footing Design:**
- Input: 1000 kN load, 200 kN/m² bearing
- Expected: Area = (1000 × 2.5) / 200 = 12.5 m²
- **Result:** ✅ PASSES

#### **Road Design:**
- Input: 5000 vehicles, 20 years, CBR 5%
- Expected: Total thickness > 300mm
- **Result:** ✅ PASSES

---

## 🚀 **Step 5: Start the Server**

### **5.1 Start Backend**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Server will start at:** http://localhost:8000
**API Docs:** http://localhost:8000/api/docs

### **5.2 Test API Endpoints**

Open browser: http://localhost:8000/api/docs

Try these endpoints:

1. **Create User:**
   ```
   POST /api/v1/auth/register
   {
     "email": "test@cedos.com",
     "username": "testuser",
     "full_name": "Test User",
     "role": "engineer",
     "password": "test123"
   }
   ```

2. **Login:**
   ```
   POST /api/v1/auth/login
   {
     "username": "testuser",
     "password": "test123"
   }
   ```

3. **Create Project:**
   ```
   POST /api/v1/projects/
   Authorization: Bearer {token}
   {
     "project_name": "Test Building",
     "project_type": "residential_building",
     "location": "Mumbai"
   }
   ```

---

## 🔍 **Step 6: Verify All Features Work**

### **6.1 Test Calculations**

```bash
# Column Design
curl -X POST "http://localhost:8000/api/v1/calculations/" \
  -H "Authorization: Bearer {token}" \
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

### **6.2 Test Advanced Features**

```bash
# Geotechnical Analysis
curl -X POST "http://localhost:8000/api/v1/geotechnical/bearing-capacity" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "soil_type": "clay",
    "cohesion": 50,
    "angle_of_internal_friction": 0,
    "unit_weight": 18,
    "foundation_depth": 1.5,
    "foundation_width": 2.0
  }'

# Hydrology
curl -X POST "http://localhost:8000/api/v1/hydrology/runoff" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "catchment_area": 1.0,
    "rainfall_intensity": 50.0,
    "runoff_coefficient": 0.7
  }'
```

---

## 📈 **Step 7: Review Test Results**

### **Success Indicators:**

✅ **All Tests Pass:**
- 9/9 unit tests passed
- All integration tests passed
- All validations passed

✅ **Calculations Correct:**
- Column sizes meet IS 456 minimums
- Safety factors are correct
- Results match engineering standards

✅ **API Working:**
- All endpoints accessible
- Authentication works
- Data persistence works

---

## 🐛 **Troubleshooting**

### **Issue 1: Database Connection Failed**

**Error:** `Connection refused` or `Authentication failed`

**Solution:**
1. Check `.env` file exists
2. Verify password is correct (no brackets)
3. Test connection:
   ```bash
   psql "postgresql://postgres:PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
   ```

### **Issue 2: Module Not Found**

**Error:** `ModuleNotFoundError: No module named 'sqlalchemy'`

**Solution:**
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### **Issue 3: Migration Errors**

**Error:** `Table already exists`

**Solution:**
```bash
# Reset database (WARNING: Deletes all data)
alembic downgrade base
alembic upgrade head
```

### **Issue 4: Test Failures**

**Error:** Some tests fail

**Solution:**
1. Check calculation logic
2. Verify input parameters
3. Review error messages
4. Run individual tests:
   ```bash
   pytest tests/test_calculations.py::TestLoadCalculationEngine::test_dead_load_calculation -v
   ```

---

## ✅ **Final Checklist**

Before considering setup complete:

- [ ] Database connected successfully
- [ ] All dependencies installed
- [ ] Migrations run successfully
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Validations pass
- [ ] Server starts without errors
- [ ] API endpoints accessible
- [ ] Can create projects
- [ ] Can perform calculations
- [ ] Results are accurate

---

## 🎉 **You're Done!**

If all checks pass, your CEDOS system is:
- ✅ Fully tested
- ✅ Properly configured
- ✅ Ready to use

**Next Steps:**
1. Explore all features
2. Create real projects
3. Test all calculations
4. Generate documents

---

## 📚 **Additional Resources**

- **Full Documentation**: See `README.md`, `RUN_INSTRUCTIONS.md`
- **API Documentation**: http://localhost:8000/api/docs
- **Test Coverage**: `pytest --cov=app --cov-report=html`

---

**Happy Testing! 🧪**
