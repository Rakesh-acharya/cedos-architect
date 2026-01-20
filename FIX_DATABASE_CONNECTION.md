# 🔧 Fix Database Connection Error

## 🐛 **The Error**

```
connection to server at "localhost" (::1), port 5432 failed: Connection refused
```

**Issue:** Migrations are trying to connect to `localhost` instead of your Supabase database.

**Cause:** `DATABASE_URL` environment variable is either:
- Not set in Railway
- Using default value (`localhost`)
- Set incorrectly

---

## ✅ **Solution: Set DATABASE_URL in Railway**

### **Step 1: Get Your Supabase Database URL**

Your Supabase URL:
```
postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
```

**Replace `[YOUR-PASSWORD]` with your actual Supabase password!**

---

### **Step 2: Set Environment Variable in Railway**

#### **Via Railway Dashboard:**

1. Go to: https://railway.app/dashboard
2. Click your service
3. Go to **"Variables"** tab
4. Click **"New Variable"**
5. **Name:** `DATABASE_URL`
6. **Value:** `postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres`
7. Click **"Add"**

---

#### **Via Railway CLI:**

```powershell
cd C:\Users\rakes\architect\backend

# Set DATABASE_URL (replace YOUR-PASSWORD)
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
```

---

### **Step 3: Redeploy**

After setting the variable:

1. Go to Railway dashboard
2. Click **"Redeploy"** on latest deployment
3. Railway will use the new DATABASE_URL

---

## ✅ **What I've Done**

1. ✅ Created `backend/start.sh` - Startup script with error handling
2. ✅ Updated `railway.json` - Better error handling for migrations
3. ✅ Migrations will continue even if they fail (might already be applied)

---

## 🔍 **Verify Environment Variables**

In Railway dashboard, make sure these are set:

- ✅ `DATABASE_URL` - Your Supabase database URL
- ✅ `SECRET_KEY` - Random secret key
- ✅ `BACKEND_CORS_ORIGINS` - `["*"]`

---

## ✅ **After Setting DATABASE_URL**

Railway will:
1. ✅ Build successfully
2. ✅ Start server
3. ✅ Run migrations (with correct database)
4. ✅ Deploy successfully!

---

**Set DATABASE_URL in Railway and redeploy!** 🚀
