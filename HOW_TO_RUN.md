# 🚀 How to Run CEDOS Web Project

## ⚡ **Easiest Method: Double-Click the Batch File**

Simply **double-click** this file:
```
run_web_project.bat
```

That's it! The script will handle everything automatically.

---

## 📝 **Alternative Methods**

### **Method 1: From Command Prompt (CMD)**

```cmd
cd C:\Users\rakes\architect
run_web_project.bat
```

Or double-click `run_web_project.bat` in File Explorer.

---

### **Method 2: From PowerShell**

If you want to use PowerShell script instead:

```powershell
# First, allow script execution (run once as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then run the script
cd C:\Users\rakes\architect
.\run_web_project.ps1
```

**Note:** If you see "Select an app to open this .ps1 file" dialog, use Method 1 (batch file) instead.

---

### **Method 3: Right-Click and Run**

1. Right-click on `run_web_project.bat`
2. Select "Run as administrator" (optional, but recommended)
3. Script will run automatically

---

## 🔐 **Login Credentials**

After the script runs, use these credentials:

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `admin` | `admin123` |
| **Engineer** | `engineer` | `engineer123` |
| **Senior Engineer** | `senior` | `senior123` |
| **Project Manager** | `manager` | `manager123` |
| **Quantity Surveyor** | `qs` | `qs123` |
| **Auditor** | `auditor` | `auditor123` |
| **Government Officer** | `govt` | `govt123` |

---

## 🌐 **Access URLs**

- **Web App:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

---

## ✅ **What Happens When You Run**

1. ✅ Checks prerequisites (Python, Node.js)
2. ✅ Sets up backend (venv, dependencies, migrations)
3. ✅ Creates default users (all 7 roles)
4. ✅ Sets up frontend (dependencies)
5. ✅ Starts backend server (new window)
6. ✅ Starts frontend server (new window)
7. ✅ Shows login credentials

**Two new windows will open** - one for backend, one for frontend.

---

## 🐛 **Troubleshooting**

### **"Python not found"**
- Install Python 3.9+ from python.org
- Make sure to check "Add Python to PATH" during installation

### **"Node.js not found"**
- Install Node.js 16+ from nodejs.org
- Restart your computer after installation

### **"Database connection failed"**
- Make sure PostgreSQL is running
- Check `backend/.env` file for correct database URL
- Or use your Supabase URL in `.env`

### **"Port already in use"**
- Stop other services using ports 3000 or 8000
- Or close the windows and restart

### **Script opens in Notepad/Editor**
- You're trying to open `.ps1` file - use `.bat` file instead
- Double-click `run_web_project.bat` instead

---

## 📁 **File Locations**

- **Batch Script:** `run_web_project.bat` (use this!)
- **PowerShell Script:** `run_web_project.ps1` (if you prefer PowerShell)
- **User Creation:** `backend/create_default_users.py`
- **Complete Guide:** `WEB_PROJECT_RUN_GUIDE.md`

---

## 🎯 **Quick Start**

1. **Double-click:** `run_web_project.bat`
2. **Wait** for setup to complete
3. **Open:** http://localhost:3000
4. **Login:** `admin` / `admin123`

**Done!** 🎉

---

**Need more help?** See `WEB_PROJECT_RUN_GUIDE.md` for detailed instructions.
