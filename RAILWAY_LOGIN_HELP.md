# 🔐 Railway Login - Browserless Method

## ✅ **Complete Railway Login**

Since browser login failed, use browserless method:

### **Step 1: Get Authentication Token**

1. Go to: https://railway.app/account/tokens
2. Click "New Token"
3. Give it a name (e.g., "cedos-deployment")
4. Copy the token (you'll only see it once!)

### **Step 2: Login with Token**

Run this command (replace YOUR_TOKEN with the token you copied):

```powershell
railway login --browserless YOUR_TOKEN
```

Or set it as environment variable:

```powershell
$env:RAILWAY_TOKEN="YOUR_TOKEN"
railway login
```

---

## 🚀 **After Login - Deploy**

Once logged in:

```powershell
cd backend
railway init
railway variables set DATABASE_URL="postgresql://postgres:YOUR-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres"
railway variables set SECRET_KEY="your-random-secret-key"
railway variables set BACKEND_CORS_ORIGINS='["*"]'
railway up
```

---

**Get your token from:** https://railway.app/account/tokens
