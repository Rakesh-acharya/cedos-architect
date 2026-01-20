# ⚡ Quick Run Guide - CEDOS Web Project

## 🚀 **Easiest Method: Double-Click**

Simply **double-click** this file:
```
run_web_project.bat
```

Or from **Command Prompt**:

```cmd
cd C:\Users\rakes\architect
run_web_project.bat
```

**Alternative (PowerShell):**

```powershell
.\run_web_project.ps1
```

**Note:** If PowerShell shows "Select an app" dialog, use the `.bat` file instead!

That's it! The script will:
- Setup everything automatically
- Create all default users
- Start both servers
- Show you login credentials

---

## 🔐 **Login Credentials**

After script runs, login with:

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
- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

---

## 📁 **Where to Run**

Run from: `C:\Users\rakes\architect\`

```powershell
cd C:\Users\rakes\architect
.\run_web_project.ps1
```

---

## ✅ **Prerequisites**

- Python 3.9+
- Node.js 16+
- PostgreSQL running
- Database accessible

---

## 🐛 **Quick Fixes**

**Script won't run?**
- Run PowerShell as Administrator
- Check you're in project root directory

**Database error?**
- Ensure PostgreSQL is running
- Check `.env` file in `backend/` folder

**Port in use?**
- Stop other services on ports 3000/8000
- Or change ports in config

---

**See `WEB_PROJECT_RUN_GUIDE.md` for detailed instructions!**
