# 🚀 Complete Deployment Guide - Step by Step

## 🎯 **Current Situation**

- ✅ Railway login attempted (need browserless method)
- ❌ Frontend can't connect (backend not running)
- ✅ Ready to deploy

---

## 📋 **Two Options**

### **Option A: Test Locally First (Recommended)**

1. **Start Backend Locally**
2. **Test Everything**
3. **Then Deploy to Railway**

### **Option B: Deploy to Railway Now**

1. **Complete Railway Login**
2. **Deploy Backend**
3. **Update Frontend**

---

## 🚀 **Option A: Start Locally First**

### **Step 1: Start Backend**

Open PowerShell and run:

```powershell
cd C:\Users\rakes\architect
.\START_BACKEND_ONLY.bat
```

**Or manually:**

```powershell
cd C:\Users\rakes\architect\backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Keep this window open!**

### **Step 2: Frontend Should Connect**

Your frontend (already running) should now connect to backend automatically.

### **Step 3: Test**

- Backend: http://localhost:8000/api/docs
- Frontend: http://localhost:3000
- Login: `admin` / `admin123`

---

## 🌐 **Option B: Deploy to Railway**

### **Step 1: Complete Railway Login**

1. Go to: https://railway.app/account/tokens
2. Click "New Token"
3. Name it: "cedos-deployment"
4. Copy the token

Then run:

```powershell
railway login --browserless YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with the token you copied.

### **Step 2: Deploy Backend**

```powershell
cd C:\Users\rakes\architect\backend

# Initialize Railway project
railway init

# Set environment variables (REPLACE YOUR-PASSWORD)
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="your-random-secret-key-here"
railway variables set BACKEND_CORS_ORIGINS='["*"]'

# Deploy
railway up

# Run migrations
railway run alembic upgrade head

# Create users
railway run python create_default_users.py

# Get your URL
railway domain
```

### **Step 3: Get Your Railway URL**

After deployment, you'll get a URL like:
```
https://cedos-backend-production.up.railway.app
```

### **Step 4: Test Railway Backend**

Open in browser:
```
https://your-url.up.railway.app/api/docs
```

Should see API documentation!

### **Step 5: Update Frontend (Optional)**

If you want frontend to use Railway backend, update API URL in frontend config.

---

## ✅ **Quick Fix Right Now**

**To fix the connection error immediately:**

1. **Open new PowerShell window**
2. **Run:**
   ```powershell
   cd C:\Users\rakes\architect
   .\START_BACKEND_ONLY.bat
   ```
3. **Keep window open**
4. **Frontend will connect automatically**

---

## 🎯 **Recommended Flow**

1. ✅ **Fix connection error** - Start backend locally
2. ✅ **Test everything** - Make sure it works
3. ✅ **Deploy to Railway** - For production access
4. ✅ **Update mobile app** - With Railway URL

---

## 📱 **After Railway Deployment**

Update mobile app:

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

Then rebuild APK - works from anywhere!

---

## 🔐 **Railway Login Token**

Get it from: https://railway.app/account/tokens

Then run:
```powershell
railway login --browserless YOUR_TOKEN
```

---

**Right now: Start backend locally to fix the connection error!**

Run: `.\START_BACKEND_ONLY.bat`
