# 🚀 pgAdmin Quick Start Guide

## ✅ **pgAdmin is 100% FREE!**

pgAdmin is **completely free** and **open source**. No cost, no subscription, no limitations!

---

## 🎯 **Quick Setup**

### **Option 1: Automated Script (Recommended)**

```powershell
.\INSTALL_PGADMIN_AUTO.bat
```

This script will:
1. ✅ Download pgAdmin installer
2. ✅ Install pgAdmin automatically
3. ✅ Create database `cedos_db`
4. ✅ Create user `cedos_user`
5. ✅ Configure `.env` file
6. ✅ Launch pgAdmin

---

### **Option 2: Manual Installation**

1. **Download:** https://www.pgadmin.org/download/
2. **Install** with default settings
3. **Launch** pgAdmin
4. **Connect** to PostgreSQL (see below)

---

## 🔌 **Connect to PostgreSQL**

### **Step 1: Launch pgAdmin**

- From **Start Menu** → Search "pgAdmin 4"
- Or double-click desktop shortcut

### **Step 2: Create Server Connection**

1. **Right-click "Servers"** (left sidebar)
2. **Click "Create"** → **"Server"**

### **Step 3: General Tab**

- **Name:** `CEDOS Local`

### **Step 4: Connection Tab**

- **Host name/address:** `localhost`
- **Port:** `5432`
- **Maintenance database:** `postgres`
- **Username:** `postgres`
- **Password:** (your PostgreSQL password)
- ✅ **Check "Save password"**

### **Step 5: Save**

- Click **"Save"**

---

## 📊 **View Your Database**

1. **Expand** `CEDOS Local` → **"Databases"**
2. **Expand** `cedos_db` → **"Schemas"** → **"public"** → **"Tables"**
3. Tables will appear after running migrations

---

## 🔍 **Run SQL Queries**

1. **Right-click** `cedos_db` → **"Query Tool"**
2. **Write SQL** in the editor
3. **Click "Execute"** (or press F5)

**Example:**
```sql
SELECT * FROM users;
```

---

## 📝 **View/Edit Data**

1. **Right-click** any table → **"View/Edit Data"** → **"All Rows"**
2. View/edit data in spreadsheet-like interface
3. Changes are saved automatically

---

## 💾 **Backup/Restore**

### **Backup:**
1. **Right-click** `cedos_db` → **"Backup"**
2. Choose format (SQL, CSV, etc.)
3. Click **"Backup"**

### **Restore:**
1. **Right-click** `cedos_db` → **"Restore"**
2. Select backup file
3. Click **"Restore"**

---

## 🎨 **Features**

- ✅ **SQL Editor** - Write and execute queries
- ✅ **Data Viewer** - View/edit data visually
- ✅ **Query History** - Track all queries
- ✅ **Backup/Restore** - Easy data management
- ✅ **User Management** - Manage users and permissions
- ✅ **Schema Browser** - Navigate database structure
- ✅ **ERD Tool** - Visualize database relationships

---

## 📋 **Database Connection Info**

```
Database: cedos_db
User: cedos_user
Password: cedos_pass
Host: localhost
Port: 5432
```

---

## 🚀 **After Setup**

1. **Run migrations:**
   ```powershell
   cd backend
   alembic upgrade head
   ```

2. **Start server:**
   ```powershell
   uvicorn app.main:app --reload
   ```

3. **Access API:**
   - API Docs: http://localhost:8000/api/docs
   - Frontend: http://localhost:3000

---

## ✅ **pgAdmin is FREE Forever!**

- ✅ **No cost** - Completely free
- ✅ **No subscription** - Use forever
- ✅ **No limitations** - Full features
- ✅ **Open source** - Community supported
- ✅ **Regular updates** - Always improving

---

## 🆘 **Troubleshooting**

### **pgAdmin won't launch:**
- Check if PostgreSQL is running
- Restart pgAdmin
- Check Windows firewall

### **Can't connect:**
- Verify PostgreSQL is running
- Check username/password
- Verify port 5432 is correct

### **Database not visible:**
- Run migrations: `alembic upgrade head`
- Refresh pgAdmin (F5)
- Check user permissions

---

## 📚 **More Resources**

- **Official Docs:** https://www.pgadmin.org/docs/
- **Download:** https://www.pgadmin.org/download/
- **Support:** https://www.pgadmin.org/support/

---

**pgAdmin is 100% FREE and perfect for PostgreSQL!** 🚀
