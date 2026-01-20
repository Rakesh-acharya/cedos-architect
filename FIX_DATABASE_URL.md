# 🔧 Fix DATABASE_URL with Special Characters

## ❌ **The Problem**

Your password contains special characters (`123#$`) that need to be **URL-encoded** in the connection string.

**Error:**
```
could not translate host name "123#$@db.zlhtegmjmlqkygmegneu.supabase.co"
```

The `#` and `$` characters are breaking the URL parsing!

---

## ✅ **The Solution**

Special characters in passwords must be **percent-encoded**:
- `#` → `%23`
- `$` → `%24`
- `@` → `%40`
- `&` → `%26`
- `%` → `%25`
- etc.

---

## 🚀 **Quick Fix (Automated)**

### **Option 1: PowerShell Script (Recommended)**

```powershell
cd C:\Users\rakes\architect
.\SET_DATABASE_URL_FIXED.ps1
```

This script will:
1. Ask for your password
2. **Automatically URL-encode** special characters
3. Set DATABASE_URL in Railway
4. Redeploy

---

### **Option 2: Batch File**

```cmd
cd C:\Users\rakes\architect
SET_DATABASE_URL_FIXED.bat
```

---

## 🔧 **Manual Fix**

### **Step 1: URL-Encode Your Password**

If your password is `123#$`, it should become `123%23%24`

**Online tool:** https://www.urlencoder.org/

**Or use PowerShell:**
```powershell
[System.Web.HttpUtility]::UrlEncode("123#$")
# Output: 123%23%24
```

---

### **Step 2: Set in Railway Dashboard**

1. Go to: https://railway.app/dashboard
2. Your service → **Variables** tab
3. Click **"New Variable"**
4. **Name:** `DATABASE_URL`
5. **Value:** `postgresql://postgres:YOUR-ENCODED-PASSWORD@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres`
   - Replace `YOUR-ENCODED-PASSWORD` with URL-encoded password
6. Click **"Add"**

---

## 📝 **Example**

**Original password:** `123#$@pass`

**URL-encoded:** `123%23%24%40pass`

**Full DATABASE_URL:**
```
postgresql://postgres:123%23%24%40pass@db.zlhtegmjmlqkygmegneu.supabase.co:5432/postgres
```

---

## ✅ **After Fixing**

Railway will:
1. ✅ Parse DATABASE_URL correctly
2. ✅ Connect to Supabase database
3. ✅ Run migrations successfully
4. ✅ Start server
5. ✅ Deploy successfully

---

## 🎯 **Quick Action**

Run this script:
```powershell
.\SET_DATABASE_URL_FIXED.ps1
```

Enter your password (with special characters). It will automatically encode and set it!

---

**The issue is URL encoding!** Use the fixed script to handle special characters automatically. 🔧
