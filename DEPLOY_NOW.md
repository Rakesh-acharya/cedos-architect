# 🚀 Deploy CEDOS Backend NOW - Step by Step

## ✅ **What You Need**

1. Your Supabase password
2. GitHub account (free)
3. 10 minutes

---

## 🎯 **Quickest Method: Railway (Recommended)**

### **Step 1: Install Railway CLI**

Open PowerShell and run:

```powershell
npm install -g @railway/cli
```

---

### **Step 2: Run Deployment Script**

I've created an automated script for you!

**Option A: Use the Batch Script (Easiest)**

```powershell
cd C:\Users\rakes\architect
.\QUICK_DEPLOY.bat
```

**Option B: Manual Commands**

```powershell
# Navigate to backend
cd backend

# Login to Railway (opens browser)
railway login

# Initialize project
railway init

# Set your Supabase database URL (replace YOUR-PASSWORD)
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

# Set secret key (random string)
railway variables set SECRET_KEY="your-random-secret-key-here"

# Set CORS (allow all)
railway variables set BACKEND_CORS_ORIGINS='["*"]'

# Deploy!
railway up

# Run migrations
railway run alembic upgrade head

# Create users
railway run python create_default_users.py

# Get your URL
railway domain
```

---

## 📋 **What Happens**

1. ✅ Backend deploys to Railway
2. ✅ Connects to your Supabase database
3. ✅ Runs migrations automatically
4. ✅ Creates default users
5. ✅ Gives you a public URL

**You'll get a URL like:** `https://cedos-backend-production.up.railway.app`

---

## ✅ **After Deployment**

### **Test Your API:**

Open in browser:
```
https://your-url.up.railway.app/api/docs
```

Should see API documentation!

### **Update Mobile App:**

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

### **Update Web App:**

If you want to use the hosted backend, update frontend API URL.

---

## 🔐 **Login Credentials**

After deployment, use these:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Engineer | `engineer` | `engineer123` |

---

## 🎯 **Quick Commands Reference**

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

# Open dashboard
railway open
```

---

## 🐛 **Troubleshooting**

### **"Railway CLI not found"**
```powershell
npm install -g @railway/cli
```

### **"Login failed"**
- Make sure you have GitHub account
- Try: `railway login --browserless`

### **"Database connection failed"**
- Check Supabase password is correct
- Make sure Supabase allows external connections

### **"Migrations failed"**
```powershell
railway run alembic upgrade head
```

---

## 📱 **Mobile App Update**

Once you have your Railway URL:

1. Edit `cedos-mobile/src/theme.ts`
2. Replace URL with your Railway URL
3. Build APK: `eas build --platform android --profile production`
4. Share APK - works from anywhere!

---

## 🎉 **You're Done!**

Your backend is now:
- ✅ Live and accessible
- ✅ Connected to Supabase
- ✅ Ready for mobile app
- ✅ Ready for web app
- ✅ Free hosting!

---

## 🚀 **Start Now**

Run this command:

```powershell
cd C:\Users\rakes\architect
.\QUICK_DEPLOY.bat
```

**Follow the prompts and you'll be live in 5 minutes!** 🎯
