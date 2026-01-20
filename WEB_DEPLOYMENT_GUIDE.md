# Web Deployment Guide - Mobile Browser Access

## ✅ Current Status

- **Backend**: ✅ Live at `https://cedos-architect-production.up.railway.app`
- **Frontend Build**: ✅ Ready for deployment
- **API Configuration**: ✅ Configured to connect to Railway backend

## 🚀 Deployment Options

### Option 1: Deploy via GitHub (Recommended - Global Access)

Since you've authorized GitHub with Vercel, deploy via the dashboard:

1. **Go to**: https://vercel.com/dashboard
2. **Click**: "Add New Project" or "Import Project"
3. **Select**: Repository `cedos-architect`
4. **Configure**:
   - **Root Directory**: `frontend`
   - **Framework Preset**: `Vite`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
5. **Add Environment Variable**:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://cedos-architect-production.up.railway.app`
6. **Click**: "Deploy"

After deployment, your web app will be accessible globally via the Vercel URL!

**Quick Script**: Run `powershell -ExecutionPolicy Bypass -File DEPLOY_VIA_GITHUB.ps1`

### Option 2: Run Locally (Same WiFi Network)

For local mobile access:

1. **Run**: `powershell -ExecutionPolicy Bypass -File RUN_LOCAL_WEB.ps1`
2. **Access from mobile**: `http://YOUR_IP:3000`
   - Your local IP will be shown when you run the script
   - Make sure your mobile device is on the same WiFi network

## 📱 Mobile Access

Once deployed, access the web app from any mobile browser:
- **Global**: Use the Vercel URL (Option 1)
- **Local**: Use `http://YOUR_IP:3000` (Option 2)

## 🔐 Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

## 🔧 Available Scripts

1. **`DEPLOY_VIA_GITHUB.ps1`** - Opens Vercel dashboard with deployment instructions
2. **`RUN_LOCAL_WEB.ps1`** - Runs dev server accessible via local IP
3. **`CHECK_WEB_DEPLOYMENT.ps1`** - Checks deployment status
4. **`COMPLETE_WEB_DEPLOYMENT.ps1`** - Complete deployment guide with all options

## 🌐 Backend API

- **API Docs**: https://cedos-architect-production.up.railway.app/api/docs
- **API Base**: https://cedos-architect-production.up.railway.app

## ✅ Verification

After deployment, verify:
1. Web app loads in browser
2. Can login with credentials
3. Can access projects and features
4. API calls work correctly

## 📝 Notes

- The frontend is configured to connect to the Railway backend automatically
- All API calls use the centralized `apiClient` in `frontend/src/api/client.ts`
- The web app is fully responsive and works on mobile browsers
