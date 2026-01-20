# 🧪 CEDOS - Comprehensive Testing Guide

## 📋 **Testing Overview**

This guide explains how to test CEDOS thoroughly, including all calculations, endpoints, and integrations.

---

## 🚀 **Quick Start Testing**

### **1. Install Dependencies**

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
pip install pytest pytest-cov requests
```

### **2. Setup Database**

Create `.env` file in `backend/`:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
SECRET_KEY=your-secret-key-here-change-in-production
```

**Note:** Replace `[YOUR-PASSWORD]` with your actual Supabase password.

### **3. Run Database Migrations**

```bash
cd backend
alembic upgrade head
```

### **4. Run Comprehensive Tests**

```bash
# Run all tests
python test_and_run.py

# Or use pytest
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

---

## 📊 **Test Categories**

### **1. Unit Tests**

Test individual calculation functions:

```bash
pytest tests/test_calculations.py -v
pytest tests/test_advanced_calculations.py -v
```

**What's Tested:**
- Load calculations (dead, live, wind, seismic)
- Structural design (footings, columns, beams, slabs)
- Road design (flexible/rigid pavements)
- Bridge design (girders, piers)
- Drainage design (storm drains, sewers)
- Geotechnical analysis (bearing capacity, slope stability)
- Hydrology (runoff, open channels)

### **2. Integration Tests**

Test complete workflows:

```bash
pytest tests/test_integration.py -v
```

**What's Tested:**
- Project creation → Calculation → BOQ → Cost Estimate
- Data consistency across modules
- API endpoint integration

### **3. Validation Tests**

Validate calculation results against engineering standards:

```python
# Column design validation
- Minimum size: 230mm per IS 456
- Steel percentage: 1-4%
- Safety factors: As per code

# Footing design validation
- Area calculation correctness
- Minimum size: 500mm
- Safety factor: 2.5

# Road design validation
- Thickness requirements per IRC 37
- Geometry per IRC 73
```

### **4. API Tests**

Test all endpoints:

```bash
# Start server first
uvicorn app.main:app --reload

# In another terminal
pytest tests/test_api.py -v
```

---

## 🎯 **Manual Testing Scenarios**

### **Scenario 1: Complete Building Design**

1. **Create Project**
   ```bash
   POST /api/v1/projects/
   {
     "project_name": "Test Building",
     "project_type": "residential_building",
     "location": "Mumbai",
     "seismic_zone": "Zone III"
   }
   ```

2. **Design Column**
   ```bash
   POST /api/v1/calculations/
   {
     "project_id": 1,
     "calculation_type": "column_design",
     "input_parameters": {
       "axial_load": 2000,
       "concrete_grade": "M25",
       "steel_grade": "Fe415"
     }
   }
   ```

3. **Generate BOQ**
   ```bash
   POST /api/v1/boq/generate/1
   ```

4. **Create Cost Estimate**
   ```bash
   POST /api/v1/cost/estimate/1
   ```

5. **Validate Results**
   - Column size >= 230mm ✅
   - Steel percentage 1-4% ✅
   - BOQ quantities > 0 ✅
   - Cost estimate > 0 ✅

### **Scenario 2: Road Design**

1. **Design Flexible Pavement**
   ```bash
   POST /api/v1/calculations/
   {
     "project_id": 1,
     "calculation_type": "road_design",
     "input_parameters": {
       "traffic_count": 5000,
       "design_life": 20,
       "subgrade_cbr": 5.0
     }
   }
   ```

2. **Validate Results**
   - Total thickness > 300mm ✅
   - Base thickness > 150mm ✅
   - Wearing course > 50mm ✅

### **Scenario 3: Geotechnical Analysis**

1. **Calculate Bearing Capacity**
   ```bash
   POST /api/v1/geotechnical/bearing-capacity
   {
     "soil_type": "clay",
     "cohesion": 50,
     "angle_of_internal_friction": 0,
     "unit_weight": 18,
     "foundation_depth": 1.5,
     "foundation_width": 2.0
   }
   ```

2. **Validate Results**
   - Safe bearing capacity > 0 ✅
   - Factor of safety = 3.0 ✅
   - Meets IS 6403 requirements ✅

---

## ✅ **Expected Test Results**

### **Unit Tests**
- All load calculations: **PASS**
- All structural designs: **PASS**
- Road/Bridge/Drainage: **PASS**
- Geotechnical: **PASS**
- Hydrology: **PASS**

### **Integration Tests**
- Project workflow: **PASS**
- Data consistency: **PASS**
- API integration: **PASS**

### **Validation Tests**
- Code compliance: **PASS**
- Safety factors: **PASS**
- Boundary conditions: **PASS**

---

## 🔍 **Debugging Failed Tests**

### **Common Issues:**

1. **Database Connection Failed**
   - Check `.env` file exists
   - Verify `DATABASE_URL` is correct
   - Test connection: `psql $DATABASE_URL`

2. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

3. **Calculation Errors**
   - Check input parameters are valid
   - Verify calculation logic
   - Review error messages

4. **API Errors**
   - Ensure server is running
   - Check CORS settings
   - Verify authentication tokens

---

## 📈 **Test Coverage Goals**

- **Unit Tests**: > 80% coverage
- **Integration Tests**: All major workflows
- **Validation Tests**: All critical calculations
- **API Tests**: All endpoints

---

## 🎉 **Success Criteria**

All tests pass when:
1. ✅ All unit tests pass
2. ✅ All integration tests pass
3. ✅ All validations pass
4. ✅ No critical errors
5. ✅ Code coverage > 80%

---

## 📚 **Additional Resources**

- **Engineering Standards**: IS 456, IRC 37, IRC 112, IS 6403
- **Testing Best Practices**: pytest documentation
- **API Testing**: FastAPI testing guide

---

**Happy Testing! 🧪**
