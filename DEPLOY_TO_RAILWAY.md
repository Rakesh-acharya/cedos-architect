# 🚀 Deploy CEDOS Backend to Railway (Free)

## ✅ **What We'll Do**

1. Deploy backend to Railway (free hosting)
2. Connect to your Supabase database
3. Get public URL
4. Update mobile app with public URL

---

## 📋 **Prerequisites**

- GitHub account (free)
- Railway account (free)
- Your Supabase database URL

---

## 🚀 **Step-by-Step Deployment**

### **Step 1: Install Railway CLI**

Open PowerShell/Command Prompt and run:

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login
```

This will open a browser window - login with GitHub.

---

### **Step 2: Initialize Railway Project**

```powershell
# Navigate to backend directory
cd backend

# Initialize Railway project
railway init

# When asked:
# - Project name: cedos-backend (or any name)
# - Environment: production
```

---

### **Step 3: Set Environment Variables**

```powershell
# Set database URL (your Supabase URL)
railway variables set DATABASE_URL="postgresql://postgres:[YOUR-PASSWORD]@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

# Set secret key (generate a random string)
railway variables set SECRET_KEY="your-super-secret-key-change-this-to-random-string"

# Set CORS origins (allow all for now, you can restrict later)
railway variables set BACKEND_CORS_ORIGINS='["*"]'
```

**Important:** Replace `[YOUR-PASSWORD]` with your actual Supabase password!

---

### **Step 4: Deploy**

```powershell
# Deploy to Railway
railway up
```

This will:
- Build your backend
- Run migrations
- Deploy to Railway
- Give you a public URL

---

### **Step 5: Get Your Public URL**

```powershell
# Get your deployment URL
railway domain
```

Or check Railway dashboard: https://railway.app

You'll get a URL like: `https://cedos-backend-production.up.railway.app`

---

### **Step 6: Run Migrations**

```powershell
# Run database migrations
railway run alembic upgrade head

# Create default users
railway run python create_default_users.py
```

---

### **Step 7: Test Your API**

Open in browser:
```
https://your-railway-url.up.railway.app/api/docs
```

Should see API documentation!

---

### **Step 8: Update Mobile App**

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

---

## 🎯 **Quick Commands**

```powershell
# Deploy
railway up

# View logs
railway logs

# Run migrations
railway run alembic upgrade head

# Create users
railway run python create_default_users.py

# Get URL
railway domain
```

---

## ✅ **After Deployment**

1. ✅ Backend is live at: `https://your-url.up.railway.app`
2. ✅ API docs at: `https://your-url.up.railway.app/api/docs`
3. ✅ Mobile app can connect from anywhere
4. ✅ Web app can connect from anywhere

---

## 🔧 **Troubleshooting**

### **"Railway CLI not found"**
```powershell
npm install -g @railway/cli
```

### **"Login failed"**
- Make sure you have GitHub account
- Try: `railway login --browserless`

### **"Database connection failed"**
- Check Supabase password is correct
- Check Supabase allows connections from Railway IPs

### **"Migrations failed"**
```powershell
railway run alembic upgrade head
```

---

## 📱 **Update Mobile App**

Once deployed, update `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

Then rebuild APK - works from anywhere!

---

**Ready to deploy? Run the commands above!** 🚀
