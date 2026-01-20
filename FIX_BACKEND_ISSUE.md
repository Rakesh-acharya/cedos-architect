# 🔧 Fix Backend Configuration Issue

## 🐛 **The Problem**

The `.env` file has incorrect format for `BACKEND_CORS_ORIGINS`. It's trying to parse it as JSON but the format is wrong.

**Error:**
```
SettingsError: error parsing value for field "BACKEND_CORS_ORIGINS"
```

---

## ✅ **Quick Fix (Choose One)**

### **Method 1: Run Fix Script (Easiest)**

Double-click or run:
```
fix_env_file.bat
```

This will automatically fix your `.env` file.

---

### **Method 2: Manual Fix**

1. **Open:** `backend/.env` file
2. **Find this line:**
   ```
   BACKEND_CORS_ORIGINS=http://localhost:3000,http://localhost:8000
   ```
3. **Replace with:**
   ```
   BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
   ```
4. **Save the file**

---

### **Method 3: Delete and Recreate**

1. **Delete:** `backend/.env` file
2. **Run:** `run_web_project.bat` again
3. It will create a new `.env` with correct format

---

## 🚀 **After Fixing**

1. **Stop backend** (if running) - Close the backend window
2. **Run fix script** or manually edit `.env`
3. **Start backend again:**
   ```cmd
   cd backend
   venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

Or just run `run_web_project.bat` again.

---

## ✅ **Verify It Works**

1. **Check backend:** http://localhost:8000/api/docs
2. **Should see API documentation**
3. **No errors** in backend window

---

## 📝 **Correct .env Format**

Your `backend/.env` should look like:

```env
# Database Configuration
DATABASE_URL=postgresql://cedos_user:cedos_pass@localhost/cedos_db

# Security
SECRET_KEY=your-secret-key-change-in-production-use-random-string

# CORS - JSON array format (IMPORTANT!)
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

**Note:** CORS origins must be in JSON array format: `["url1","url2"]`

---

## 🎯 **After Fix**

- ✅ Backend will start successfully
- ✅ Frontend can connect
- ✅ Mobile app can connect (with correct IP)
- ✅ All features work

---

**Run `fix_env_file.bat` now to fix it automatically!** 🔧
