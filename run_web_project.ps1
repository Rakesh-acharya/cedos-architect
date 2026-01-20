# ============================================================
# CEDOS Web Project - Complete Setup & Run Script
# ============================================================
# This script will:
# 1. Setup backend (venv, dependencies, migrations)
# 2. Setup frontend (dependencies)
# 3. Create default users for all roles
# 4. Start backend and frontend servers
# ============================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  CEDOS - Civil Engineering Digital Operating System" -ForegroundColor Cyan
Write-Host "  Web Project Setup & Run Script" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Get the project root directory (where this script is located)
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendDir = Join-Path $ProjectRoot "backend"
$FrontendDir = Join-Path $ProjectRoot "frontend"

# Check if directories exist
if (-not (Test-Path $BackendDir)) {
    Write-Host "[ERROR] Backend directory not found: $BackendDir" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Yellow
    exit 1
}

if (-not (Test-Path $FrontendDir)) {
    Write-Host "[ERROR] Frontend directory not found: $FrontendDir" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory." -ForegroundColor Yellow
    exit 1
}

# ============================================================
# STEP 1: Check Prerequisites
# ============================================================
Write-Host "[STEP 1] Checking Prerequisites..." -ForegroundColor Yellow
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  [OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Python not found. Please install Python 3.9+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  [OK] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  [FAIL] Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Check PostgreSQL (optional check)
Write-Host "  [INFO] Ensure PostgreSQL is running and database is accessible" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# STEP 2: Backend Setup
# ============================================================
Write-Host "[STEP 2] Setting up Backend..." -ForegroundColor Yellow
Write-Host ""

Set-Location $BackendDir

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "  Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "  [OK] Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "  [OK] Virtual environment already exists" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "  Activating virtual environment..." -ForegroundColor Cyan
$venvActivate = Join-Path $BackendDir "venv\Scripts\Activate.ps1"
if (Test-Path $venvActivate) {
    & $venvActivate
} else {
    Write-Host "  [WARN] Could not activate venv automatically. Please activate manually:" -ForegroundColor Yellow
    Write-Host "    .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
}

# Install dependencies
Write-Host "  Installing Python dependencies..." -ForegroundColor Cyan
pip install -q --upgrade pip
pip install -q -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "  [FAIL] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "  [WARN] .env file not found. Creating from defaults..." -ForegroundColor Yellow
    Write-Host "  Please update .env with your database credentials if needed" -ForegroundColor Yellow
    
    # Create basic .env file
    @"
# Database Configuration
DATABASE_URL=postgresql://cedos_user:cedos_pass@localhost/cedos_db

# Security
SECRET_KEY=your-secret-key-change-in-production-use-random-string

# CORS (comma-separated)
BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "  [OK] .env file created" -ForegroundColor Green
} else {
    Write-Host "  [OK] .env file exists" -ForegroundColor Green
}

# Run database migrations
Write-Host "  Running database migrations..." -ForegroundColor Cyan
alembic upgrade head
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Database migrations completed" -ForegroundColor Green
} else {
    Write-Host "  [WARN] Migration failed. Ensure database is running and accessible." -ForegroundColor Yellow
    Write-Host "  You can run migrations manually later: alembic upgrade head" -ForegroundColor Yellow
}

Write-Host ""

# ============================================================
# STEP 3: Create Default Users
# ============================================================
Write-Host "[STEP 3] Creating Default Users..." -ForegroundColor Yellow
Write-Host ""

# Check if create_users.py exists, if not create it
$createUsersScript = Join-Path $BackendDir "create_default_users.py"
if (-not (Test-Path $createUsersScript)) {
    Write-Host "  Creating user setup script..." -ForegroundColor Cyan
    
    @"
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash

def create_default_users():
    db = SessionLocal()
    
    # Default users for each role
    default_users = [
        {
            'email': 'admin@cedos.com',
            'username': 'admin',
            'full_name': 'System Administrator',
            'role': UserRole.ADMIN,
            'password': 'admin123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'engineer@cedos.com',
            'username': 'engineer',
            'full_name': 'Civil Engineer',
            'role': UserRole.ENGINEER,
            'password': 'engineer123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'senior@cedos.com',
            'username': 'senior',
            'full_name': 'Senior Engineer',
            'role': UserRole.SENIOR_ENGINEER,
            'password': 'senior123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'manager@cedos.com',
            'username': 'manager',
            'full_name': 'Project Manager',
            'role': UserRole.PROJECT_MANAGER,
            'password': 'manager123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'qs@cedos.com',
            'username': 'qs',
            'full_name': 'Quantity Surveyor',
            'role': UserRole.QUANTITY_SURVEYOR,
            'password': 'qs123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'auditor@cedos.com',
            'username': 'auditor',
            'full_name': 'Auditor',
            'role': UserRole.AUDITOR,
            'password': 'auditor123',
            'is_active': True,
            'is_verified': True
        },
        {
            'email': 'govt@cedos.com',
            'username': 'govt',
            'full_name': 'Government Officer',
            'role': UserRole.GOVERNMENT_OFFICER,
            'password': 'govt123',
            'is_active': True,
            'is_verified': True
        }
    ]
    
    created_count = 0
    skipped_count = 0
    
    for user_data in default_users:
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user_data['email']) | 
            (User.username == user_data['username'])
        ).first()
        
        if existing_user:
            print(f\"  [SKIP] User already exists: {user_data['username']} ({user_data['role'].value})\")
            skipped_count += 1
            continue
        
        # Create user
        user = User(
            email=user_data['email'],
            username=user_data['username'],
            full_name=user_data['full_name'],
            role=user_data['role'],
            hashed_password=get_password_hash(user_data['password']),
            is_active=user_data['is_active'],
            is_verified=user_data['is_verified']
        )
        
        db.add(user)
        created_count += 1
        print(f\"  [OK] Created user: {user_data['username']} ({user_data['role'].value})\")
    
    db.commit()
    db.close()
    
    print(f\"\")
    print(f\"  Summary: Created {created_count} users, Skipped {skipped_count} users\")
    print(f\"  [OK] Default users setup complete!\")

if __name__ == '__main__':
    try:
        create_default_users()
    except Exception as e:
        print(f\"  [ERROR] Failed to create users: {e}\")
        print(f\"  Make sure database is running and migrations are applied.\")
        sys.exit(1)
"@ | Out-File -FilePath $createUsersScript -Encoding UTF8
    Write-Host "  [OK] User setup script created" -ForegroundColor Green
}

# Run user creation script
Write-Host "  Creating default users..." -ForegroundColor Cyan
python create_default_users.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "  [OK] Default users created successfully" -ForegroundColor Green
} else {
    Write-Host "  [WARN] User creation had issues. You can create users manually later." -ForegroundColor Yellow
}

Write-Host ""

# ============================================================
# STEP 4: Frontend Setup
# ============================================================
Write-Host "[STEP 4] Setting up Frontend..." -ForegroundColor Yellow
Write-Host ""

Set-Location $FrontendDir

# Install dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing Node.js dependencies..." -ForegroundColor Cyan
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  [OK] Frontend dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "  [FAIL] Failed to install frontend dependencies" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  [OK] Frontend dependencies already installed" -ForegroundColor Green
}

Write-Host ""

# ============================================================
# STEP 5: Display Login Credentials
# ============================================================
Write-Host "[STEP 5] Login Credentials" -ForegroundColor Yellow
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  DEFAULT USER CREDENTIALS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  ADMIN (Full Access):" -ForegroundColor Green
Write-Host "    Username: admin" -ForegroundColor White
Write-Host "    Password: admin123" -ForegroundColor White
Write-Host "    Email: admin@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  ENGINEER:" -ForegroundColor Green
Write-Host "    Username: engineer" -ForegroundColor White
Write-Host "    Password: engineer123" -ForegroundColor White
Write-Host "    Email: engineer@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  SENIOR ENGINEER:" -ForegroundColor Green
Write-Host "    Username: senior" -ForegroundColor White
Write-Host "    Password: senior123" -ForegroundColor White
Write-Host "    Email: senior@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  PROJECT MANAGER:" -ForegroundColor Green
Write-Host "    Username: manager" -ForegroundColor White
Write-Host "    Password: manager123" -ForegroundColor White
Write-Host "    Email: manager@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  QUANTITY SURVEYOR:" -ForegroundColor Green
Write-Host "    Username: qs" -ForegroundColor White
Write-Host "    Password: qs123" -ForegroundColor White
Write-Host "    Email: qs@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  AUDITOR:" -ForegroundColor Green
Write-Host "    Username: auditor" -ForegroundColor White
Write-Host "    Password: auditor123" -ForegroundColor White
Write-Host "    Email: auditor@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "  GOVERNMENT OFFICER:" -ForegroundColor Green
Write-Host "    Username: govt" -ForegroundColor White
Write-Host "    Password: govt123" -ForegroundColor White
Write-Host "    Email: govt@cedos.com" -ForegroundColor Gray
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================
# STEP 6: Start Servers
# ============================================================
Write-Host "[STEP 6] Starting Servers..." -ForegroundColor Yellow
Write-Host ""
Write-Host "  Backend will start at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Frontend will start at: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "  API Documentation: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in new window
Write-Host "  Starting Backend Server..." -ForegroundColor Cyan
Set-Location $BackendDir
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in new window
Write-Host "  Starting Frontend Server..." -ForegroundColor Cyan
Set-Location $FrontendDir
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$FrontendDir'; npm run dev"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  [SUCCESS] Servers are starting!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Backend: http://localhost:8000" -ForegroundColor White
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "  Login with any of the credentials above!" -ForegroundColor Yellow
Write-Host ""
Write-Host "  To stop servers, close the PowerShell windows or press Ctrl+C" -ForegroundColor Gray
Write-Host ""

# Return to project root
Set-Location $ProjectRoot
