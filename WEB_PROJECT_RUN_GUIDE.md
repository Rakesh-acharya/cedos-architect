# 🚀 CEDOS Web Project - Complete Run Guide

## 📋 **Quick Start**

### **Method 1: Batch File (Easiest - Recommended)**

Simply **double-click** this file:
```
run_web_project.bat
```

Or from **Command Prompt**:

```cmd
cd C:\Users\rakes\architect
run_web_project.bat
```

### **Method 2: PowerShell Script**

If you prefer PowerShell:

```powershell
# First, allow script execution (run once as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run the script
.\run_web_project.ps1
```

**Note:** If you see "Select an app to open this .ps1 file" dialog, use Method 1 (batch file) instead!

This script will:
- ✅ Setup backend (venv, dependencies, migrations)
- ✅ Setup frontend (dependencies)
- ✅ Create default users for all roles
- ✅ Start both backend and frontend servers
- ✅ Display login credentials

---

## 📁 **Directory Structure**

```
architect/
├── backend/              # Backend (FastAPI)
├── frontend/             # Frontend (React)
├── run_web_project.ps1   # Run script (THIS FILE)
└── WEB_PROJECT_RUN_GUIDE.md
```

---

## 🎯 **Where to Run**

### **Run from Project Root:**

```powershell
# Navigate to project root
cd C:\Users\rakes\architect

# Run the script
.\run_web_project.ps1
```

**Important:** Run the script from the **project root directory** (where `backend` and `frontend` folders are).

---

## 🔐 **Login Credentials**

After running the script, you can login with any of these accounts:

### **1. ADMIN (Full Access)**
- **Username:** `admin`
- **Password:** `admin123`
- **Email:** admin@cedos.com
- **Role:** Administrator
- **Access:** All features, full system control

### **2. ENGINEER**
- **Username:** `engineer`
- **Password:** `engineer123`
- **Email:** engineer@cedos.com
- **Role:** Civil Engineer
- **Access:** Create projects, perform calculations, view reports

### **3. SENIOR ENGINEER**
- **Username:** `senior`
- **Password:** `senior123`
- **Email:** senior@cedos.com
- **Role:** Senior Engineer
- **Access:** All engineer features + approve designs, review calculations

### **4. PROJECT MANAGER**
- **Username:** `manager`
- **Password:** `manager123`
- **Email:** manager@cedos.com
- **Role:** Project Manager
- **Access:** Manage projects, track progress, view reports, manage team

### **5. QUANTITY SURVEYOR**
- **Username:** `qs`
- **Password:** `qs123`
- **Email:** qs@cedos.com
- **Role:** Quantity Surveyor
- **Access:** BOQ generation, cost estimation, material quantities

### **6. AUDITOR**
- **Username:** `auditor`
- **Password:** `auditor123`
- **Email:** auditor@cedos.com
- **Role:** Auditor
- **Access:** View all projects, audit logs, compliance reports

### **7. GOVERNMENT OFFICER**
- **Username:** `govt`
- **Password:** `govt123`
- **Email:** govt@cedos.com
- **Role:** Government Officer
- **Access:** View public projects, compliance verification, approvals

---

## 🌐 **Access URLs**

After running the script:

- **Frontend (Web App):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## 📝 **Manual Setup (If Script Fails)**

### **Step 1: Backend Setup**

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Create default users
python create_default_users.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### **Step 2: Frontend Setup** (New Terminal)

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start frontend server
npm run dev
```

---

## 🔧 **Prerequisites**

Before running, ensure you have:

- ✅ **Python 3.9+** installed
- ✅ **Node.js 16+** installed
- ✅ **PostgreSQL** installed and running
- ✅ **Database** created and accessible

### **Check Prerequisites:**

```powershell
# Check Python
python --version

# Check Node.js
node --version

# Check PostgreSQL (if psql is in PATH)
psql --version
```

---

## 🗄️ **Database Configuration**

### **Default Database Settings:**

- **Database:** `cedos_db`
- **User:** `cedos_user`
- **Password:** `cedos_pass`
- **Host:** `localhost`
- **Port:** `5432`

### **Create Database (if needed):**

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE cedos_db;

-- Create user
CREATE USER cedos_user WITH PASSWORD 'cedos_pass';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE cedos_db TO cedos_user;

-- Exit
\q
```

### **Update Database URL:**

Edit `backend/.env` file:

```env
DATABASE_URL=postgresql://cedos_user:cedos_pass@localhost/cedos_db
```

Or use your Supabase URL:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
```

---

## 🐛 **Troubleshooting**

### **Issue: "Backend directory not found"**
- ✅ Run script from project root directory
- ✅ Ensure `backend` folder exists

### **Issue: "Python not found"**
- ✅ Install Python 3.9+ from python.org
- ✅ Add Python to PATH

### **Issue: "Node.js not found"**
- ✅ Install Node.js 16+ from nodejs.org
- ✅ Add Node.js to PATH

### **Issue: "Database connection failed"**
- ✅ Ensure PostgreSQL is running
- ✅ Check database credentials in `.env`
- ✅ Verify database exists

### **Issue: "Migration failed"**
- ✅ Ensure database is accessible
- ✅ Check database URL in `.env`
- ✅ Run manually: `cd backend && alembic upgrade head`

### **Issue: "Port already in use"**
- ✅ Stop other services using ports 3000 or 8000
- ✅ Or change ports in configuration

### **Issue: "Users already exist"**
- ✅ This is normal - script skips existing users
- ✅ To recreate users, delete them from database first

---

## 📚 **User Roles Explained**

### **ADMIN**
- Full system access
- User management
- System configuration
- All features unlocked

### **ENGINEER**
- Create and manage projects
- Perform calculations
- Generate reports
- View own projects

### **SENIOR ENGINEER**
- All Engineer features
- Approve designs
- Review calculations
- Mentor junior engineers

### **PROJECT MANAGER**
- Manage multiple projects
- Track progress
- Team management
- Resource allocation
- Reports and analytics

### **QUANTITY SURVEYOR**
- Generate BOQ
- Cost estimation
- Material quantities
- Rate analysis

### **AUDITOR**
- View all projects
- Audit logs
- Compliance verification
- Generate audit reports

### **GOVERNMENT OFFICER**
- View public projects
- Compliance verification
- Approve projects
- Regulatory oversight

---

## ✅ **Verification Steps**

After running the script:

1. **Check Backend:**
   - Open: http://localhost:8000/api/docs
   - Should see API documentation

2. **Check Frontend:**
   - Open: http://localhost:3000
   - Should see login page

3. **Test Login:**
   - Use credentials: `admin` / `admin123`
   - Should successfully login

4. **Test API:**
   - Login via API: http://localhost:8000/api/v1/auth/login
   - Should receive access token

---

## 🎉 **Success!**

If everything works:
- ✅ Backend running on port 8000
- ✅ Frontend running on port 3000
- ✅ Can login with any credentials
- ✅ Can create projects
- ✅ Can perform calculations

**You're ready to use CEDOS!**

---

## 📞 **Need Help?**

- Check `RUN_INSTRUCTIONS.md` for detailed setup
- Check `FINAL_COMPLETE_GUIDE.md` for complete documentation
- Review error messages in PowerShell windows
- Check database connection
- Verify all prerequisites are installed

---

**Happy Engineering! 🏗️**
