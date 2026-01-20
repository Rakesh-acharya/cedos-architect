# 🚀 Deploy CEDOS Backend to Render (Free Alternative)

## ✅ **What We'll Do**

1. Deploy backend to Render (free hosting)
2. Connect to your Supabase database
3. Get public URL
4. Update mobile app with public URL

---

## 📋 **Prerequisites**

- GitHub account (free)
- Render account (free) - sign up at render.com
- Your Supabase database URL

---

## 🚀 **Step-by-Step Deployment**

### **Step 1: Push Code to GitHub**

If not already done:

```powershell
# Initialize git (if not already)
cd backend
git init
git add .
git commit -m "Initial commit"

# Create GitHub repo and push
# (Do this via GitHub website or GitHub CLI)
```

---

### **Step 2: Create Render Service**

1. Go to: https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your `backend` folder

---

### **Step 3: Configure Service**

**Settings:**

- **Name:** `cedos-backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt && alembic upgrade head`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Environment Variables:**

Add these:
```
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
SECRET_KEY=your-super-secret-key-change-this-to-random-string
BACKEND_CORS_ORIGINS=["*"]
```

---

### **Step 4: Deploy**

Click "Create Web Service"

Render will:
- Build your backend
- Run migrations
- Deploy
- Give you a URL

---

### **Step 5: Get Your Public URL**

After deployment, you'll get a URL like:
```
https://cedos-backend.onrender.com
```

---

### **Step 6: Run Migrations**

Go to Render dashboard → Your service → Shell:

```bash
alembic upgrade head
python create_default_users.py
```

---

### **Step 7: Test Your API**

Open in browser:
```
https://your-url.onrender.com/api/docs
```

---

## ✅ **After Deployment**

1. ✅ Backend is live
2. ✅ API docs available
3. ✅ Mobile app can connect
4. ✅ Web app can connect

---

**Render is free but may sleep after inactivity. Railway is better for always-on!**
