# 🚀 Deploy via Railway Web Interface (No CLI Needed!)

## ✅ **Easiest Method - Use Railway Web Dashboard**

Since CLI token authentication is having issues, use Railway's web interface:

---

## 📋 **Step-by-Step (5 Minutes)**

### **Step 1: Go to Railway**

Open: https://railway.app/new

### **Step 2: Create New Project**

Click **"New Project"** → **"Empty Project"**

### **Step 3: Add Service**

1. Click **"Add Service"**
2. Select **"GitHub Repo"**
3. Connect your GitHub account (if not connected)
4. Select your repository
5. Select **"backend"** folder as root directory

**OR** if you don't have GitHub:

1. Click **"Add Service"**
2. Select **"Empty Service"**
3. We'll configure it manually

### **Step 4: Configure Service**

#### **A. Set Build Command**

In Railway dashboard → Your service → **Settings**:

- **Build Command:** `pip install -r requirements.txt && alembic upgrade head`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### **B. Set Environment Variables**

Go to **Variables** tab, add:

```
DATABASE_URL = postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
SECRET_KEY = your-random-secret-key-here
BACKEND_CORS_ORIGINS = ["*"]
```

**Replace `YOUR-PASSWORD` with your Supabase password!**

### **Step 5: Deploy**

Railway will automatically:
- ✅ Build your backend
- ✅ Install dependencies
- ✅ Run migrations
- ✅ Start the server
- ✅ Give you a URL

### **Step 6: Get Your URL**

1. Go to **Settings** tab
2. Click **"Generate Domain"**
3. Copy your URL (e.g., `https://cedos-backend.up.railway.app`)

### **Step 7: Run Migrations & Create Users**

Go to **Deployments** tab → Click on latest deployment → **View Logs**

Or use **Shell** tab:

```bash
alembic upgrade head
python create_default_users.py
```

---

## ✅ **After Deployment**

1. ✅ Backend is live!
2. ✅ Test: `https://your-url.up.railway.app/api/docs`
3. ✅ Update mobile app with URL
4. ✅ Done!

---

## 🎯 **Quick Summary**

1. Go to: https://railway.app/new
2. Create Empty Project
3. Add GitHub Repo (select backend folder)
4. Set environment variables
5. Railway auto-deploys
6. Get URL from Settings

**No CLI needed!** 🎉

---

## 📱 **Update Mobile App**

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

---

**This method is easier and doesn't require CLI!** ✅
