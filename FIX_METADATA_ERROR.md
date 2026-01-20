# 🔧 Fix SQLAlchemy Reserved Name Error

## 🐛 **The Error**

```
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.
```

**Location:** `backend/app/models/advanced_features.py` - `IoTReading` class

**Issue:** `metadata` is a reserved name in SQLAlchemy (used for table metadata).

---

## ✅ **Fixed!**

**Changed:**
```python
# Before
metadata = Column(JSON)  # Additional sensor data

# After
sensor_metadata = Column(JSON)  # Additional sensor data (renamed from 'metadata' - reserved in SQLAlchemy)
```

**File:** `backend/app/models/advanced_features.py` (line 39)

---

## 🚀 **Pushed to GitHub**

The fix has been:
- ✅ Applied
- ✅ Committed
- ✅ Pushed to GitHub

Railway will automatically redeploy!

---

## ✅ **What Will Happen**

Railway will:
1. ✅ Pull latest code
2. ✅ Build successfully
3. ✅ Run migrations successfully
4. ✅ Deploy successfully!

---

**Check Railway dashboard - deployment should succeed now!** 🚀
