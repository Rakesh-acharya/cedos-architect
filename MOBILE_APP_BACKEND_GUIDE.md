# 📱 Mobile App - Backend Connection Guide

## 🔌 **How Mobile App Connects to Backend**

### **Important Understanding:**

The mobile app **does NOT** have its own database or backend. It connects to the **same backend** that the web app uses.

---

## 🌐 **Connection Methods**

### **Method 1: Local Development (Testing)**

When developing/testing on your phone:

1. **Backend runs on your computer** (localhost:8000)
2. **Phone and computer must be on same WiFi network**
3. **Use your computer's IP address** instead of localhost

**Configuration:**

Edit `cedos-mobile/src/theme.ts`:

```typescript
export const API_BASE_URL = __DEV__ 
  ? 'http://192.168.1.100:8000/api/v1'  // YOUR computer's IP
  : 'https://your-api-url.com/api/v1';   // Production URL
```

**To find your computer's IP:**
- Windows: Run `ipconfig` → Look for "IPv4 Address"
- Example: `192.168.1.100`

**Steps:**
1. Start backend on your computer: `run_web_project.bat`
2. Find your computer's IP address
3. Update mobile app's `API_BASE_URL` with your IP
4. Connect phone to same WiFi
5. Run mobile app (Expo Go or built APK)

---

### **Method 2: Production (Deployed Backend)**

For sharing with friends or production use:

1. **Deploy backend to cloud** (Heroku, AWS, Railway, etc.)
2. **Get public URL** (e.g., `https://cedos-api.herokuapp.com`)
3. **Update mobile app** with production URL
4. **Build APK** with production URL
5. **Share APK** - works from anywhere!

**Configuration:**

```typescript
export const API_BASE_URL = 'https://your-deployed-api.com/api/v1';
```

---

## 🚀 **Deployment Options**

### **Option 1: Heroku (Easiest)**

1. Create account at heroku.com
2. Install Heroku CLI
3. Deploy backend:

```bash
cd backend
heroku create cedos-api
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
```

4. Get URL: `https://cedos-api.herokuapp.com`
5. Update mobile app with this URL

### **Option 2: Railway**

1. Create account at railway.app
2. Connect GitHub repository
3. Deploy backend
4. Get public URL
5. Update mobile app

### **Option 3: AWS/Google Cloud**

More complex but more control. See deployment guides.

---

## 📱 **Mobile App Configuration**

### **For Development (Local Testing):**

```typescript
// cedos-mobile/src/theme.ts
export const API_BASE_URL = __DEV__ 
  ? 'http://YOUR_COMPUTER_IP:8000/api/v1'
  : 'https://your-api-url.com/api/v1';
```

**Example:**
```typescript
export const API_BASE_URL = __DEV__ 
  ? 'http://192.168.1.100:8000/api/v1'
  : 'https://cedos-api.herokuapp.com/api/v1';
```

### **For Production (APK):**

```typescript
// cedos-mobile/src/theme.ts
export const API_BASE_URL = 'https://your-deployed-api.com/api/v1';
```

**Then build APK:**
```bash
eas build --platform android --profile production
```

---

## ✅ **Current Setup (Your Situation)**

### **Right Now:**

- ✅ Backend runs on: `http://localhost:8000`
- ✅ Web app connects to: `http://localhost:3000`
- ✅ Mobile app needs: Your computer's IP address

### **To Test Mobile App Locally:**

1. **Start backend:** Run `run_web_project.bat`
2. **Find your IP:** Run `ipconfig` → Get IPv4 Address
3. **Update mobile app:** Edit `cedos-mobile/src/theme.ts`:
   ```typescript
   export const API_BASE_URL = 'http://YOUR_IP:8000/api/v1';
   ```
4. **Connect phone to same WiFi**
5. **Run mobile app** (Expo Go or APK)

---

## 🔒 **Security Notes**

### **For Production:**

1. **Use HTTPS** (not HTTP)
2. **Add authentication** (already implemented)
3. **Use environment variables** for API URLs
4. **Enable CORS** properly (already configured)

### **Current CORS Setup:**

Backend allows:
- `http://localhost:3000` (web app)
- `http://localhost:8000` (API docs)
- Your mobile app's origin (when deployed)

**To add mobile app origin:**

Edit `backend/.env`:
```env
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","*"]
```

Or for production:
```env
BACKEND_CORS_ORIGINS=["https://your-web-app.com","https://your-mobile-app.com"]
```

---

## 🐛 **Troubleshooting**

### **"Network Error" in Mobile App**

- ✅ Check backend is running
- ✅ Check phone and computer on same WiFi
- ✅ Check IP address is correct
- ✅ Check firewall allows port 8000
- ✅ Try accessing `http://YOUR_IP:8000/api/docs` from phone browser

### **"Connection Refused"**

- ✅ Backend not running - start it with `run_web_project.bat`
- ✅ Wrong IP address - check with `ipconfig`
- ✅ Firewall blocking - allow port 8000

### **"CORS Error"**

- ✅ Add mobile app origin to `BACKEND_CORS_ORIGINS` in `.env`
- ✅ Restart backend after changing `.env`

---

## 📋 **Summary**

### **For Testing (Now):**
1. Backend runs on your computer
2. Mobile app connects via your computer's IP
3. Both on same WiFi network

### **For Sharing (Production):**
1. Deploy backend to cloud
2. Update mobile app with cloud URL
3. Build APK
4. Share APK - works from anywhere!

---

## 🎯 **Next Steps**

1. **Fix current backend issue** (see fix instructions)
2. **Test web app** first
3. **Then configure mobile app** for local testing
4. **Later deploy backend** for production use

---

**The mobile app is just a frontend - it needs the backend to work!** 🏗️
