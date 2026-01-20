# 🔧 Fix Frontend Connection Error

## 🐛 **The Problem**

Frontend is trying to connect to backend at `http://localhost:8000` but backend is not running.

**Error:**
```
http proxy error: /api/v1/projects/
AggregateError [ECONNREFUSED]
```

---

## ✅ **Solution: Choose One**

### **Option 1: Start Backend Locally (For Testing)**

Run backend on your computer:

```powershell
# Navigate to backend
cd backend

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Or use the batch script:**
```powershell
cd C:\Users\rakes\architect
.\run_web_project.bat
```

This will start both backend and frontend.

---

### **Option 2: Deploy to Railway (For Production)**

1. **Complete Railway login** (see RAILWAY_LOGIN_HELP.md)
2. **Deploy backend** to Railway
3. **Get Railway URL**
4. **Update frontend** to use Railway URL

---

## 🎯 **Quick Fix (Right Now)**

### **Start Backend Locally:**

Open a **new PowerShell window** and run:

```powershell
cd C:\Users\rakes\architect\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Keep this window open!**

Then your frontend (running in the other window) will connect successfully.

---

## ✅ **Verify It Works**

1. Backend running: http://localhost:8000/api/docs
2. Frontend running: http://localhost:3000
3. Frontend should connect to backend automatically

---

## 🚀 **For Production (Railway)**

After deploying to Railway:

1. Get Railway URL: `https://your-app.up.railway.app`
2. Update frontend API URL (if needed)
3. Frontend will connect to Railway backend

---

**Right now: Start backend locally to fix the connection error!**
