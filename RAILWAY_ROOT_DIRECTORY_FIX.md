# 🚀 Railway Root Directory Fix - Quick Guide

## ⚠️ **Issue**

Railway can't find your Python app because it's looking in the root directory, but your backend is in `backend/` folder.

---

## ✅ **Quick Fix (30 Seconds)**

### **In Railway Dashboard:**

1. **Go to:** Your Railway project → Your service
2. **Click:** "Settings" tab
3. **Find:** "Root Directory" field
4. **Change:** From `/` to `/backend`
5. **Click:** "Save"
6. **Wait:** Railway will auto-redeploy

**That's it!** ✅

---

## 📋 **Detailed Steps**

### **Step 1: Open Railway Dashboard**

https://railway.app/dashboard

### **Step 2: Select Your Service**

Click on the service that failed to deploy

### **Step 3: Go to Settings**

Click the **"Settings"** tab at the top

### **Step 4: Change Root Directory**

Scroll down to find **"Root Directory"** field

**Current:** `/` (or empty)  
**Change to:** `/backend`

### **Step 5: Save**

Click **"Save"** button

### **Step 6: Wait for Redeploy**

Railway will automatically:
- ✅ Detect Python in `backend/` folder
- ✅ Build your app
- ✅ Deploy successfully

---

## ✅ **What Happens After Fix**

Railway will now:
- ✅ Look in `backend/` folder
- ✅ Find `requirements.txt`
- ✅ Detect Python app
- ✅ Install dependencies
- ✅ Run `alembic upgrade head` (from railway.json)
- ✅ Start server with `uvicorn`
- ✅ Deploy successfully!

---

## 🎯 **Verify It Works**

After redeploy:

1. Check **"Deployments"** tab
2. Latest deployment should show **"Build succeeded"**
3. Get your URL from **"Settings"** → **"Domains"**
4. Test: `https://your-url.up.railway.app/api/docs`

---

## 📝 **Configuration Files**

I've created:
- ✅ `backend/nixpacks.toml` - Helps Railway detect Python
- ✅ `backend/railway.json` - Build configuration

These help Railway understand your app structure.

---

## 🔄 **If Still Fails**

1. **Check Root Directory** is set to `/backend`
2. **Check Build Command** in Settings:
   - Should be: `pip install -r requirements.txt && alembic upgrade head`
3. **Check Start Command**:
   - Should be: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. **Check Variables** are set correctly

---

**Just change Root Directory to `/backend` and you're done!** 🎉
