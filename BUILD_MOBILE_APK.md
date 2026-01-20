# 📱 Build CEDOS Mobile APK - Complete Guide

## 🚀 **Quick Build (Automated)**

Run this script:

```powershell
cd C:\Users\rakes\cedos-mobile
.\BUILD_APK_SIMPLE.bat
```

This will:
1. ✅ Ask for Railway URL
2. ✅ Update API configuration
3. ✅ Install dependencies
4. ✅ Build APK
5. ✅ Give you download link

---

## 📋 **Step-by-Step**

### **Step 1: Get Railway Backend URL**

1. Go to: https://railway.app/dashboard
2. Click your service
3. Go to **Settings** tab
4. Scroll to **"Domains"** section
5. Copy the URL (e.g., `https://cedos-backend-production.up.railway.app`)

**OR** generate one:
- Click **"Generate Domain"**
- Copy the generated URL

---

### **Step 2: Run Build Script**

```powershell
cd C:\Users\rakes\cedos-mobile
.\BUILD_APK_SIMPLE.bat
```

Enter your Railway URL when asked.

---

### **Step 3: Login to Expo**

The script will open a browser:
- If you have Expo account: Login
- If not: Create free account at https://expo.dev

---

### **Step 4: Wait for Build**

- Takes 10-15 minutes
- Builds in the cloud
- You'll see progress in terminal

---

### **Step 5: Download APK**

After build completes:
1. Go to: https://expo.dev
2. Click your profile → **"View builds"**
3. Find latest build
4. Click **"Download"** button
5. Download the APK file

---

### **Step 6: Install on Android**

1. **Transfer APK** to your phone (USB, email, cloud)
2. **Enable Unknown Sources:**
   - Settings → Security → Unknown Sources (Enable)
   - OR Settings → Apps → Special access → Install unknown apps
3. **Open APK file** on phone
4. **Click Install**
5. **Open app** and login!

---

## 🔧 **Manual Update API URL**

If you need to change API URL manually:

```powershell
cd C:\Users\rakes\cedos-mobile
.\UPDATE_API_URL.bat
```

Or edit `src/theme.ts`:

```typescript
export const API_BASE_URL = 'https://your-railway-url.up.railway.app/api/v1';
```

---

## ✅ **Configuration**

### **What's Configured:**

- ✅ API URL (updates automatically from Railway URL)
- ✅ CORS (already set in backend)
- ✅ Authentication (JWT tokens)
- ✅ All API endpoints
- ✅ Error handling
- ✅ Offline support (caching)

### **Backend Requirements:**

- ✅ Backend deployed on Railway
- ✅ CORS allows mobile app
- ✅ Database connected
- ✅ Users created

---

## 🔐 **Login Credentials**

Use these in the mobile app:

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `admin123` |
| Engineer | `engineer` | `engineer123` |

---

## 🐛 **Troubleshooting**

### **"EAS CLI not found"**
```powershell
npm install -g eas-cli
```

### **"Login failed"**
```powershell
eas login
```
Or create account at: https://expo.dev

### **"Build failed"**
- Check internet connection
- Make sure Railway URL is correct
- Check Expo dashboard for errors

### **"Can't install APK"**
- Enable "Unknown Sources" in Android settings
- Check APK downloaded completely
- Try downloading again

### **"App won't connect to backend"**
- Verify Railway URL is correct
- Check backend is running (test in browser)
- Check CORS settings in backend

---

## 📱 **After Installation**

1. ✅ Open app on phone
2. ✅ Login with credentials
3. ✅ Create projects
4. ✅ Use calculator
5. ✅ Everything works!

---

## 🎯 **Quick Reference**

**Build APK:**
```powershell
cd C:\Users\rakes\cedos-mobile
.\BUILD_APK_SIMPLE.bat
```

**Update API URL:**
```powershell
.\UPDATE_API_URL.bat
```

**Check Build Status:**
- https://expo.dev → View builds

---

## ✅ **What's Included in APK**

- ✅ All features from web app
- ✅ Login/authentication
- ✅ Project management
- ✅ Calculator
- ✅ Dashboard
- ✅ File management
- ✅ Connected to Railway backend
- ✅ Works offline (with cached data)

---

**Run `.\BUILD_APK_SIMPLE.bat` to build your APK!** 🚀
