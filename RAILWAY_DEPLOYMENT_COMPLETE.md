# 🚀 Complete Railway Deployment Guide

## ✅ **Automated Deployment Script**

I've created scripts to automatically:
1. ✅ Run database migrations
2. ✅ Deploy backend to Railway
3. ✅ Configure environment variables
4. ✅ Make your app globally accessible

---

## 🎯 **Quick Deploy**

### **Option 1: Complete Automated Deployment**

```powershell
.\DEPLOY_TO_RAILWAY_COMPLETE.bat
```

This script will:
1. ✅ Check prerequisites
2. ✅ Login to Railway (if needed)
3. ✅ Initialize Railway project
4. ✅ Setup Supabase database
5. ✅ Configure environment variables
6. ✅ Run migrations automatically
7. ✅ Deploy to Railway
8. ✅ Get public URL
9. ✅ Create default users

---

### **Option 2: Quick Deploy (Minimal Steps)**

```powershell
.\QUICK_DEPLOY_RAILWAY.bat
```

Faster version with minimal prompts.

---

## 📋 **Step-by-Step Manual Deployment**

### **Step 1: Install Railway CLI**

```powershell
npm install -g @railway/cli
```

### **Step 2: Login to Railway**

```powershell
railway login
```

### **Step 3: Initialize Project**

```powershell
cd backend
railway init
```

### **Step 4: Setup Database**

```powershell
# Set Supabase connection string
railway variables set DATABASE_URL="postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres"
```

### **Step 5: Setup Environment Variables**

```powershell
railway variables set SECRET_KEY="your-secret-key-here"
railway variables set BACKEND_CORS_ORIGINS="[\"*\"]"
```

### **Step 6: Run Migrations**

```powershell
railway run alembic upgrade head
```

### **Step 7: Deploy**

```powershell
railway up
```

### **Step 8: Get Public URL**

```powershell
railway domain
```

---

## 🔧 **Environment Variables**

Required variables in Railway:

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `postgresql://...` | Supabase connection string |
| `SECRET_KEY` | Random string | JWT secret key |
| `BACKEND_CORS_ORIGINS` | `["*"]` | CORS allowed origins |

---

## 📊 **After Deployment**

### **Access Your API:**

- **API Base:** `https://your-app.railway.app`
- **API Docs:** `https://your-app.railway.app/api/docs`
- **Health Check:** `https://your-app.railway.app/health`

### **Default Users:**

**Admin:**
- Username: `admin`
- Password: `admin123`

**Engineer:**
- Username: `engineer`
- Password: `engineer123`

---

## 🌐 **Make Frontend Use Railway Backend**

### **Update Frontend Config:**

Edit `frontend/src/config.ts`:

```typescript
export const API_URL = 'https://your-app.railway.app';
```

### **Deploy Frontend:**

```powershell
.\DEPLOY_FRONTEND_VERCEL.bat
```

---

## 🔍 **Verify Deployment**

### **1. Check Railway Dashboard**

Go to: https://railway.app/dashboard

- ✅ Service should show "Active"
- ✅ Logs should show "Uvicorn running"
- ✅ No errors in logs

### **2. Test API**

```powershell
# Health check
curl https://your-app.railway.app/health

# API docs
# Open: https://your-app.railway.app/api/docs
```

### **3. Test Database**

```powershell
# Run a query via Railway
railway run python -c "from app.core.database import engine; print('Connected!' if engine.connect() else 'Failed')"
```

---

## 🐛 **Troubleshooting**

### **Migrations Failed**

```powershell
# Check logs
railway logs

# Run migrations manually
railway run alembic upgrade head
```

### **Database Connection Failed**

1. Verify `DATABASE_URL` is correct:
   ```powershell
   railway variables
   ```

2. Check Supabase project is active
3. Verify connection string format

### **Deployment Failed**

1. Check Railway logs:
   ```powershell
   railway logs
   ```

2. Verify all dependencies in `requirements.txt`
3. Check `railway.json` configuration

---

## ✅ **Deployment Checklist**

- [ ] Railway CLI installed
- [ ] Logged in to Railway
- [ ] Project initialized
- [ ] DATABASE_URL set (Supabase)
- [ ] SECRET_KEY set
- [ ] BACKEND_CORS_ORIGINS set
- [ ] Migrations run successfully
- [ ] Deployment successful
- [ ] Public URL obtained
- [ ] API accessible
- [ ] Frontend updated with backend URL

---

## 🚀 **Quick Start**

**Just run:**

```powershell
.\DEPLOY_TO_RAILWAY_COMPLETE.bat
```

Follow the prompts and your app will be globally accessible!

---

**Your CEDOS backend will be live globally in minutes!** 🌍
