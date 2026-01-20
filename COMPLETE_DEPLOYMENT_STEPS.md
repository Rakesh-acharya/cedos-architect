# 🚀 Complete Deployment Steps - Follow These

## ✅ **What You Need**

1. Railway account (free)
2. Your Supabase password
3. 10 minutes

---

## 📋 **Step-by-Step Instructions**

### **Step 1: Login to Railway**

Open PowerShell and run:

```powershell
railway login
```

This will open a browser - login with GitHub.

**OR** if that doesn't work:

1. Go to: https://railway.app/account/tokens
2. Create new token
3. Copy the token
4. Run: `railway login --browserless YOUR_TOKEN`

---

### **Step 2: Navigate to Backend**

```powershell
cd C:\Users\rakes\architect\backend
```

---

### **Step 3: Initialize Railway Project**

```powershell
railway init --name cedos-backend
```

When asked:
- Project name: `cedos-backend` (or press Enter)
- Environment: `production` (or press Enter)

---

### **Step 4: Set Environment Variables**

**You'll need your Supabase password here!**

```powershell
# Set database URL (REPLACE YOUR-PASSWORD with your actual Supabase password)
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"

# Set secret key (random string)
railway variables set SECRET_KEY="cedos-secret-key-$(Get-Random)"

# Set CORS (allow all origins)
railway variables set BACKEND_CORS_ORIGINS='["*"]'
```

---

### **Step 5: Deploy**

```powershell
railway up
```

This takes 3-5 minutes. Wait for it to complete.

---

### **Step 6: Run Migrations**

```powershell
railway run alembic upgrade head
```

---

### **Step 7: Create Users**

```powershell
railway run python create_default_users.py
```

---

### **Step 8: Get Your URL**

```powershell
railway domain
```

Copy the URL - this is your live backend!

---

### **Step 9: Test**

Open in browser:
```
https://your-url.up.railway.app/api/docs
```

Should see API documentation!

---

## 🎯 **Quick Script (After Login)**

Once you're logged in, run:

```powershell
cd C:\Users\rakes\architect
.\DEPLOY_WITH_PASSWORD.bat
```

It will ask for your Supabase password and do everything automatically.

---

## ✅ **After Deployment**

1. ✅ Backend is live
2. ✅ Connected to Supabase
3. ✅ Migrations run
4. ✅ Users created
5. ✅ Ready to use!

---

## 📱 **Update Mobile App**

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

Then rebuild APK!

---

**Start with Step 1: `railway login`**
