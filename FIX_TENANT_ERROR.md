# 🔧 Fix: "Tenant or user not found" Error

## ❌ **New Error**

The error changed from "password authentication failed" to **"Tenant or user not found"**.

This means:
- ✅ Password might be correct now
- ❌ But connection string format is wrong!

---

## ✅ **The Problem**

Supabase **pooler** connection requires a **different username format**:

**Wrong:**
```
postgresql://postgres:PASSWORD@pooler-host:6543/postgres
```

**Correct:**
```
postgresql://postgres.PROJECT_REF:PASSWORD@pooler-host:6543/postgres
```

The username must be `postgres.PROJECT_REF` not just `postgres`!

---

## 🚀 **Quick Fix**

### **Option 1: Use Correct Pooler Format**

Run this script:
```powershell
.\FIX_SUPABASE_POOLER_FORMAT.bat
```

It will:
1. Ask for your PROJECT REF
2. Construct correct connection string
3. Update Railway
4. Test connection

---

### **Option 2: Get Connection String from Supabase**

Run this script:
```powershell
.\GET_SUPABASE_CONNECTION_STRING.bat
```

It opens Supabase dashboard and shows you where to find the correct connection string.

---

## 📋 **Manual Fix Steps**

### **Step 1: Get PROJECT REF**

1. Go to: https://supabase.com/dashboard
2. Your project → **Settings** → **Database**
3. Look for **"Connection Pooling"** tab
4. Find connection string like:
   ```
   postgres://postgres.abcdefgh:PASSWORD@...
   ```
5. The `abcdefgh` part is your PROJECT REF

---

### **Step 2: Construct Correct Connection String**

**Format:**
```
postgresql://postgres.PROJECT_REF:ENCODED_PASSWORD@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```

**Example:**
```
postgresql://postgres.abcdefgh:Rakesh%40123%23%24@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
```

---

### **Step 3: Update Railway**

**Via Railway Dashboard:**
1. Go to: https://railway.app/dashboard
2. Your service → **Variables** tab
3. Update `DATABASE_URL` with correct format
4. Click **Save**

**Via CLI:**
```powershell
railway variables set DATABASE_URL="postgresql://postgres.PROJECT_REF:Rakesh%40123%23%24@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
```

---

## 🔄 **Alternative: Use Direct Connection**

If pooler keeps failing, use **direct connection**:

1. Supabase dashboard → **Settings** → **Database**
2. Copy **"Connection string"** (not pooler)
3. Format: `postgresql://postgres:PASSWORD@db.xxx.supabase.co:5432/postgres`
4. Use this in Railway instead

**Direct connection format:**
```
postgresql://postgres:Rakesh%40123%23%24@db.xxx.supabase.co:5432/postgres
```

(No PROJECT_REF needed for direct connection)

---

## ✅ **After Fixing**

Railway will:
1. ✅ Accept the connection string
2. ✅ Connect successfully
3. ✅ Run migrations
4. ✅ Start server

---

## 🎯 **Quick Action**

**Run this:**
```powershell
.\FIX_SUPABASE_POOLER_FORMAT.bat
```

Enter your PROJECT REF when asked. The script will fix everything!

---

**The "Tenant or user not found" error will be fixed!** 🔧
