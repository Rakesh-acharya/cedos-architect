# 🔌 pgAdmin Connection Guide - Step by Step

## 📋 **Connection Details**

For your CEDOS project:

```
Name: CEDOS Local
Host: localhost
Port: 5432
Database: postgres (for initial connection)
Username: postgres
Password: [Your PostgreSQL postgres user password]
```

---

## 🚀 **Step-by-Step Configuration**

### **Step 1: General Tab**

1. **Name:** Enter `CEDOS Local`
   - This is just a friendly name for your connection
   - Can be anything you want

2. **Server group:** Leave as `Servers` (default)

3. **Connect now?:** Toggle ON (blue) ✅
   - This will connect immediately after saving

4. Click **"Save"** button

---

### **Step 2: Connection Tab**

After clicking Save, pgAdmin will ask for connection details:

1. **Host name/address:** `localhost`
   - For local PostgreSQL installation

2. **Port:** `5432`
   - Default PostgreSQL port

3. **Maintenance database:** `postgres`
   - Use this for initial connection

4. **Username:** `postgres`
   - Your PostgreSQL superuser

5. **Password:** [Enter your PostgreSQL postgres password]
   - The password you set during PostgreSQL installation
   - ✅ Check "Save password" to avoid entering it every time

6. Click **"Save"** button

---

### **Step 3: Verify Connection**

After saving, pgAdmin will:
- ✅ Connect to PostgreSQL
- ✅ Show "CEDOS Local" in the left sidebar
- ✅ Expand to show databases

---

### **Step 4: View Your Database**

1. **Expand** `CEDOS Local` → **"Databases"**
2. You should see:
   - `cedos_db` (your CEDOS database)
   - `postgres` (default database)
   - `template0`, `template1` (system databases)

---

### **Step 5: Connect to cedos_db**

1. **Expand** `cedos_db` → **"Schemas"** → **"public"** → **"Tables"**
2. Tables will appear after running migrations:
   ```powershell
   cd backend
   alembic upgrade head
   ```

---

## 🔧 **If Connection Fails**

### **Error: "Connection refused"**
- ✅ Check PostgreSQL is running
- ✅ Verify port 5432 is correct
- ✅ Check Windows Firewall

### **Error: "Password authentication failed"**
- ✅ Verify postgres password is correct
- ✅ Try resetting PostgreSQL password

### **Error: "Database does not exist"**
- ✅ Create database first:
  ```sql
  CREATE DATABASE cedos_db;
  ```

---

## 📝 **Quick Reference**

### **For Local PostgreSQL:**
```
Name: CEDOS Local
Host: localhost
Port: 5432
Username: postgres
Password: [Your PostgreSQL password]
Database: postgres (for connection)
```

### **For Supabase (Cloud):**
```
Name: CEDOS Supabase
Host: db.xxx.supabase.co
Port: 5432
Username: postgres
Password: [Your Supabase password]
Database: postgres
```

---

## ✅ **After Connection**

Once connected, you can:
- ✅ View all databases
- ✅ Run SQL queries
- ✅ View/edit data
- ✅ Manage users
- ✅ Backup/restore

---

**Follow these steps to connect pgAdmin to your PostgreSQL!** 🚀
