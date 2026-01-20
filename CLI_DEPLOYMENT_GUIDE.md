# 🚀 Railway CLI Deployment - Complete Guide

## ✅ **Using CLI Commands (No Web Interface)**

All deployment done via command line!

---

## 📋 **Quick Start**

### **Method 1: Automated Script (Easiest)**

```powershell
cd C:\Users\rakes\architect
.\DEPLOY_CLI_SIMPLE.bat
```

This script:
- Navigates to backend folder (sets correct root directory)
- Logs into Railway
- Sets all variables
- Deploys
- Runs migrations
- Creates users

---

### **Method 2: Manual CLI Commands**

```powershell
# Step 1: Navigate to backend folder (IMPORTANT!)
cd C:\Users\rakes\architect\backend

# Step 2: Login to Railway
railway login

# Step 3: Link to project (or create new)
railway link
# If no project exists:
# railway init

# Step 4: Set environment variables
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="your-secret-key-here"
railway variables set BACKEND_CORS_ORIGINS='["*"]'

# Step 5: Deploy
railway up

# Step 6: Run migrations
railway run alembic upgrade head

# Step 7: Create users
railway run python create_default_users.py

# Step 8: Get URL
railway domain
```

---

## 🔑 **Key Point: Root Directory**

**IMPORTANT:** Always run Railway CLI commands from the `backend` folder!

This automatically sets the root directory correctly.

```powershell
# ✅ CORRECT - Run from backend folder
cd backend
railway up

# ❌ WRONG - Don't run from root
cd ..
railway up  # This won't find your Python app
```

---

## 📝 **Complete CLI Commands Reference**

### **Login**
```powershell
railway login
# Opens browser for authentication

# Or with token:
railway login --browserless YOUR_TOKEN
```

### **Project Management**
```powershell
# Link to existing project
railway link

# Create new project
railway init --name cedos-backend

# List projects
railway projects
```

### **Environment Variables**
```powershell
# Set variable
railway variables set VARIABLE_NAME="value"

# View variables
railway variables

# Delete variable
railway variables delete VARIABLE_NAME
```

### **Deployment**
```powershell
# Deploy
railway up

# View logs
railway logs

# Open dashboard
railway open
```

### **Run Commands**
```powershell
# Run command in Railway environment
railway run python create_default_users.py

# Run migrations
railway run alembic upgrade head

# Run any command
railway run COMMAND
```

### **Get Information**
```powershell
# Get deployment URL
railway domain

# Generate domain
railway domain generate

# View service info
railway status
```

---

## 🎯 **Step-by-Step Deployment**

### **1. Navigate to Backend**
```powershell
cd C:\Users\rakes\architect\backend
```

### **2. Login**
```powershell
railway login
```

### **3. Initialize Project**
```powershell
railway init --name cedos-backend
```

### **4. Set Variables**
```powershell
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="cedos-secret-key-$(Get-Random)"
railway variables set BACKEND_CORS_ORIGINS='["*"]'
```

### **5. Deploy**
```powershell
railway up
```

### **6. Post-Deploy**
```powershell
railway run alembic upgrade head
railway run python create_default_users.py
```

### **7. Get URL**
```powershell
railway domain
```

---

## ✅ **Why CLI from Backend Folder Works**

When you run `railway up` from the `backend` folder:
- ✅ Railway detects Python automatically
- ✅ Finds `requirements.txt`
- ✅ Finds `railway.json` and `nixpacks.toml`
- ✅ Sets root directory correctly
- ✅ Builds and deploys successfully

---

## 🔧 **Troubleshooting**

### **"Not logged in"**
```powershell
railway login
```

### **"Project not found"**
```powershell
railway link
# Or
railway init
```

### **"Build failed"**
- Make sure you're in `backend` folder
- Check `requirements.txt` exists
- Check variables are set

### **"Deployment failed"**
```powershell
# Check logs
railway logs

# Redeploy
railway up
```

---

## 📚 **Useful CLI Commands**

```powershell
# View all commands
railway --help

# View service status
railway status

# View logs
railway logs --tail

# Open in browser
railway open

# List all services
railway services
```

---

## 🎯 **Quick Deploy Script**

Just run:
```powershell
.\DEPLOY_CLI_SIMPLE.bat
```

It does everything automatically!

---

**All via CLI - No web interface needed!** 🚀
