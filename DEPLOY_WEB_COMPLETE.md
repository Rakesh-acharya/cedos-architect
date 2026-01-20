# 🚀 Complete Web-Based Deployment (No CLI!)

## ✅ **Easiest Method - Railway Web Dashboard**

This method uses Railway's web interface - **no CLI needed!**

---

## 📋 **Complete Steps (10 Minutes)**

### **Step 1: Go to Railway**

Open: https://railway.app/new

Login with GitHub if needed.

---

### **Step 2: Create New Project**

1. Click **"New Project"**
2. Select **"Empty Project"**
3. Name it: `cedos-backend` (optional)

---

### **Step 3: Add Your Backend**

#### **Option A: From GitHub (Recommended)**

1. Click **"Add Service"**
2. Select **"GitHub Repo"**
3. If first time: **Connect GitHub** → Authorize Railway
4. Select your repository (the one with `backend` folder)
5. **Root Directory:** Select `backend` folder
6. Click **"Deploy"**

#### **Option B: Manual Upload**

1. Click **"Add Service"**
2. Select **"Empty Service"**
3. We'll configure manually (see below)

---

### **Step 4: Configure Service**

Go to your service → **Settings** tab:

#### **Build Settings:**

- **Build Command:** 
  ```
  pip install -r requirements.txt && alembic upgrade head
  ```

- **Start Command:**
  ```
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

#### **Environment Variables:**

Go to **Variables** tab, click **"New Variable"**, add these:

**Variable 1:**
- **Name:** `DATABASE_URL`
- **Value:** `postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres`
- **Replace `YOUR-PASSWORD` with your actual Supabase password!**

**Variable 2:**
- **Name:** `SECRET_KEY`
- **Value:** `cedos-secret-key-change-in-production`

**Variable 3:**
- **Name:** `BACKEND_CORS_ORIGINS`
- **Value:** `["*"]`

---

### **Step 5: Deploy**

Railway will automatically:
- ✅ Clone your code
- ✅ Install dependencies
- ✅ Run migrations
- ✅ Start server
- ✅ Give you a URL

**Wait 3-5 minutes for deployment.**

---

### **Step 6: Get Your URL**

1. Go to **Settings** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"**
4. Copy your URL (e.g., `https://cedos-backend-production.up.railway.app`)

---

### **Step 7: Create Users**

Go to **Deployments** tab → Click latest deployment → **View Logs**

Or use **Shell** tab:

1. Click **"Shell"** tab
2. Run:
   ```bash
   python create_default_users.py
   ```

---

### **Step 8: Test**

Open in browser:
```
https://your-url.up.railway.app/api/docs
```

Should see API documentation! ✅

---

## ✅ **You're Done!**

Your backend is now:
- ✅ Live and accessible
- ✅ Connected to Supabase
- ✅ Users created
- ✅ Ready for mobile app

---

## 📱 **Update Mobile App**

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

Then rebuild APK!

---

## 🎯 **Quick Checklist**

- [ ] Go to https://railway.app/new
- [ ] Create Empty Project
- [ ] Add GitHub Repo (select backend folder)
- [ ] Set DATABASE_URL (with Supabase password)
- [ ] Set SECRET_KEY
- [ ] Set BACKEND_CORS_ORIGINS = ["*"]
- [ ] Wait for deployment
- [ ] Generate domain
- [ ] Run `python create_default_users.py` in Shell
- [ ] Test API docs
- [ ] Update mobile app

---

**This method is easier and more reliable than CLI!** 🎉
