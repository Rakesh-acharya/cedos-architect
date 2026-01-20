# ============================================================
#   BUILD CEDOS MOBILE APK
#   Generates APK in root folder - Ready to install!
# ============================================================

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  CEDOS - Building Mobile APK" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

$ErrorActionPreference = "Stop"

# Railway URL
$RAILWAY_URL = "https://cedos-architect-production.up.railway.app"

Write-Host "Railway Backend: $RAILWAY_URL" -ForegroundColor Cyan
Write-Host ""

# Check Expo login first
Write-Host "Checking Expo login..." -ForegroundColor Cyan
$easCheck = eas whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Not logged in to Expo!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please login first by running this in a NEW terminal window:" -ForegroundColor Yellow
    Write-Host "  eas login" -ForegroundColor White
    Write-Host ""
    Write-Host "Then enter:" -ForegroundColor Yellow
    Write-Host "  Email: rakeshacherya123@gmail.com" -ForegroundColor White
    Write-Host "  Password: Rakesh@123#$" -ForegroundColor White
    Write-Host ""
    Write-Host "After login, run this script again:" -ForegroundColor Yellow
    Write-Host "  .\BUILD_APK.ps1" -ForegroundColor White
    Write-Host ""
    exit 1
}

$expoUser = eas whoami
Write-Host "[OK] Logged in as: $expoUser" -ForegroundColor Green
Write-Host ""

# Step 1: Setup Mobile App
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 1: Setting up Mobile App" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

if (-not (Test-Path "cedos-mobile")) {
    Write-Host "Creating mobile app directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path "cedos-mobile" | Out-Null
    Set-Location "cedos-mobile"
    
    Write-Host "Initializing Expo project..." -ForegroundColor Cyan
    npx create-expo-app@latest . --template blank-typescript --yes
    
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    npm install axios @react-navigation/native @react-navigation/native-stack react-native-paper @react-native-async-storage/async-storage
} else {
    Set-Location "cedos-mobile"
    Write-Host "Mobile app directory exists, updating..." -ForegroundColor Cyan
    npm install axios @react-navigation/native @react-navigation/native-stack react-native-paper @react-native-async-storage/async-storage
}

# Step 2: Configure API
Write-Host ""
Write-Host "Configuring API for Railway backend..." -ForegroundColor Cyan

if (-not (Test-Path "src")) {
    New-Item -ItemType Directory -Path "src" | Out-Null
}
if (-not (Test-Path "src\config")) {
    New-Item -ItemType Directory -Path "src\config" | Out-Null
}

$apiConfig = @"
export const API_BASE_URL = '$RAILWAY_URL/api/v1';

export default API_BASE_URL;
"@

Set-Content -Path "src\config\api.ts" -Value $apiConfig

Write-Host "[OK] API configured: $RAILWAY_URL/api/v1" -ForegroundColor Green

# Step 3: Create app.json
Write-Host ""
Write-Host "Creating app configuration..." -ForegroundColor Cyan

$appJson = @{
    expo = @{
        name = "CEDOS"
        slug = "cedos-mobile"
        version = "1.0.0"
        orientation = "portrait"
        icon = "./assets/icon.png"
        userInterfaceStyle = "light"
        splash = @{
            image = "./assets/splash.png"
            resizeMode = "contain"
            backgroundColor = "#1976d2"
        }
        android = @{
            package = "com.cedos.app"
            adaptiveIcon = @{
                foregroundImage = "./assets/adaptive-icon.png"
                backgroundColor = "#1976d2"
            }
            permissions = @()
        }
    }
}

$appJson | ConvertTo-Json -Depth 10 | Set-Content -Path "app.json"

Write-Host "[OK] App configuration created" -ForegroundColor Green

# Step 4: Create EAS build config
Write-Host ""
Write-Host "Creating EAS build configuration..." -ForegroundColor Cyan

$easJson = @{
    build = @{
        production = @{
            android = @{
                buildType = "apk"
            }
        }
    }
}

$easJson | ConvertTo-Json -Depth 10 | Set-Content -Path "eas.json"

Write-Host "[OK] EAS configuration created" -ForegroundColor Green

# Step 5: Create complete App.tsx
Write-Host ""
Write-Host "Creating mobile app with login and projects..." -ForegroundColor Cyan

$appCode = @"
import React, { useState, useEffect } from 'react';
import { StyleSheet, Text, View, SafeAreaView, ScrollView, TextInput, Alert } from 'react-native';
import { PaperProvider, Card, Button } from 'react-native-paper';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import API_BASE_URL from './src/config/api';

interface Project {
  id: number;
  project_name: string;
  project_type: string;
  location: string;
}

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    checkLogin();
  }, []);

  const checkLogin = async () => {
    try {
      const savedToken = await AsyncStorage.getItem('token');
      if (savedToken) {
        setToken(savedToken);
        setLoggedIn(true);
        loadProjects(savedToken);
      }
    } catch (error) {
      console.error('Error checking login:', error);
    }
  };

  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Error', 'Please enter username and password');
      return;
    }

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post(`$RAILWAY_URL/api/v1/auth/login`, formData);
      const accessToken = response.data.access_token;
      
      await AsyncStorage.setItem('token', accessToken);
      setToken(accessToken);
      setLoggedIn(true);
      loadProjects(accessToken);
    } catch (error: any) {
      Alert.alert('Login Failed', error.response?.data?.detail || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  const loadProjects = async (authToken: string) => {
    try {
      const response = await axios.get(`$RAILWAY_URL/api/v1/projects/`, {
        headers: { Authorization: `Bearer ${authToken}` }
      });
      setProjects(response.data);
    } catch (error) {
      console.error('Error loading projects:', error);
    }
  };

  const handleLogout = async () => {
    await AsyncStorage.removeItem('token');
    setLoggedIn(false);
    setToken(null);
    setProjects([]);
    setUsername('');
    setPassword('');
  };

  if (!loggedIn) {
    return (
      <PaperProvider>
        <SafeAreaView style={styles.container}>
          <ScrollView contentContainerStyle={styles.loginContainer}>
            <Text style={styles.title}>CEDOS</Text>
            <Text style={styles.subtitle}>Civil Engineering Digital Operating System</Text>
            
            <Card style={styles.card}>
              <Card.Content>
                <TextInput
                  style={styles.input}
                  placeholder="Username"
                  value={username}
                  onChangeText={setUsername}
                  autoCapitalize="none"
                />
                <TextInput
                  style={styles.input}
                  placeholder="Password"
                  value={password}
                  onChangeText={setPassword}
                  secureTextEntry
                />
                <Button
                  mode="contained"
                  onPress={handleLogin}
                  loading={loading}
                  style={styles.loginButton}
                >
                  Login
                </Button>
              </Card.Content>
            </Card>
            
            <Text style={styles.info}>API: $RAILWAY_URL</Text>
          </ScrollView>
        </SafeAreaView>
      </PaperProvider>
    );
  }

  return (
    <PaperProvider>
      <SafeAreaView style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>CEDOS</Text>
          <Button mode="text" onPress={handleLogout}>Logout</Button>
        </View>
        
        <ScrollView style={styles.content}>
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.sectionTitle}>My Projects ({projects.length})</Text>
              {projects.length === 0 ? (
                <Text style={styles.emptyText}>No projects yet. Create one from the web app!</Text>
              ) : (
                projects.map((project) => (
                  <View key={project.id} style={styles.projectItem}>
                    <Text style={styles.projectName}>{project.project_name}</Text>
                    <Text style={styles.projectType}>{project.project_type}</Text>
                    <Text style={styles.projectLocation}>{project.location}</Text>
                  </View>
                ))
              )}
            </Card.Content>
          </Card>
          
          <Card style={styles.card}>
            <Card.Content>
              <Text style={styles.sectionTitle}>Quick Actions</Text>
              <Button mode="contained" style={styles.actionButton} onPress={() => Alert.alert('Info', 'Use web app for full features')}>
                View Dashboard
              </Button>
              <Button mode="outlined" style={styles.actionButton} onPress={() => Alert.alert('Info', 'Use web app for full features')}>
                Create Project
              </Button>
              <Button mode="outlined" style={styles.actionButton} onPress={() => Alert.alert('Info', 'Use web app for full features')}>
                Calculator
              </Button>
            </Card.Content>
          </Card>
        </ScrollView>
      </SafeAreaView>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loginContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#1976d2',
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
    marginBottom: 30,
  },
  card: {
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    padding: 12,
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  loginButton: {
    marginTop: 10,
  },
  info: {
    fontSize: 12,
    color: '#999',
    textAlign: 'center',
    marginTop: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 16,
    backgroundColor: '#1976d2',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
  },
  content: {
    flex: 1,
    padding: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  projectItem: {
    padding: 12,
    backgroundColor: '#f9f9f9',
    borderRadius: 8,
    marginBottom: 10,
  },
  projectName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  projectType: {
    fontSize: 14,
    color: '#666',
    marginBottom: 3,
  },
  projectLocation: {
    fontSize: 12,
    color: '#999',
  },
  emptyText: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
    textAlign: 'center',
    padding: 20,
  },
  actionButton: {
    marginBottom: 10,
  },
});
"@

Set-Content -Path "App.tsx" -Value $appCode

Write-Host "[OK] App code created" -ForegroundColor Green

# Step 6: Initialize EAS Project (skip check, project already linked)
Write-Host ""
Write-Host "EAS project already configured" -ForegroundColor Green

# Step 7: Check Credentials
Write-Host ""
Write-Host "Checking Android credentials..." -ForegroundColor Cyan

$credentialsCheck = eas credentials --platform android 2>&1
if ($credentialsCheck -match "No credentials" -or $credentialsCheck -match "not set up") {
    Write-Host ""
    Write-Host "[ERROR] Android credentials not configured!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set up credentials first:" -ForegroundColor Yellow
    Write-Host "  1. Go to: https://expo.dev/accounts/rakeshacherya/projects/cedos-mobile" -ForegroundColor White
    Write-Host "  2. Go to 'Credentials' section" -ForegroundColor White
    Write-Host "  3. Click 'Set up credentials' for Android" -ForegroundColor White
    Write-Host "  4. Select 'Let Expo manage credentials'" -ForegroundColor White
    Write-Host ""
    Write-Host "OR run: eas credentials --platform android" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "[OK] Credentials configured" -ForegroundColor Green

# Step 8: Build APK
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 2: Building APK" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

if (-not (Get-Command eas -ErrorAction SilentlyContinue)) {
    Write-Host "Installing EAS CLI..." -ForegroundColor Cyan
    npm install -g eas-cli
}

Write-Host "Starting APK build..." -ForegroundColor Cyan
Write-Host "This will take 10-15 minutes..." -ForegroundColor Yellow
Write-Host ""

# Build APK (APK builds don't require keystore, so we can skip credentials setup)
$buildOutput = eas build --platform android --profile production --non-interactive 2>&1 | Tee-Object -Variable buildOutputText

Write-Host $buildOutputText

# Extract build ID
$buildId = ""
if ($buildOutputText -match "build ID: (\w+)") {
    $buildId = $matches[1]
} elseif ($buildOutputText -match "Build ID: (\w+)") {
    $buildId = $matches[1]
}

if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host ""
    Write-Host "Getting latest build ID..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    try {
        $buildList = eas build:list --platform android --limit 1 --json 2>&1 | ConvertFrom-Json
        if ($buildList -and $buildList.Count -gt 0) {
            $buildId = $buildList[0].id
        }
    } catch {
        Write-Host "[INFO] Build started! Check status at:" -ForegroundColor Yellow
        Write-Host "  https://expo.dev/accounts/[your-account]/builds" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Once build completes, download the APK manually." -ForegroundColor Yellow
        exit 0
    }
}

if ([string]::IsNullOrWhiteSpace($buildId)) {
    Write-Host ""
    Write-Host "[INFO] Build started! Check status at:" -ForegroundColor Yellow
    Write-Host "  https://expo.dev/accounts/[your-account]/builds" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Once build completes, download the APK manually." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Build ID: $buildId" -ForegroundColor Cyan

# Step 7: Wait for build and download APK
Write-Host ""
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host "  Step 3: Waiting for Build & Downloading APK" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Yellow
Write-Host ""

Set-Location ".."

$apkPath = Join-Path (Get-Location) "cedos.apk"

Write-Host "Waiting for build to complete..." -ForegroundColor Cyan
Write-Host "This may take 10-15 minutes..." -ForegroundColor Yellow
Write-Host ""

$maxAttempts = 90
$attempt = 0
$buildComplete = $false
$downloadUrl = ""

Set-Location "cedos-mobile"

while ($attempt -lt $maxAttempts -and -not $buildComplete) {
    Start-Sleep -Seconds 10
    $attempt++
    
    Write-Host "Checking build status... ($attempt/$maxAttempts)" -ForegroundColor Gray
    
    try {
        $buildInfo = eas build:view $buildId --json 2>&1 | ConvertFrom-Json
        
        if ($buildInfo.status -eq "finished") {
            $buildComplete = $true
            $downloadUrl = $buildInfo.artifacts.buildUrl
            Write-Host ""
            Write-Host "[OK] Build completed!" -ForegroundColor Green
            break
        } elseif ($buildInfo.status -eq "errored") {
            Write-Host ""
            Write-Host "[ERROR] Build failed!" -ForegroundColor Red
            Write-Host "Check: https://expo.dev/accounts/[your-account]/builds/$buildId" -ForegroundColor Yellow
            exit 1
        } elseif ($buildInfo.status -eq "in-progress") {
            Write-Host "  Status: Building..." -ForegroundColor Yellow
        }
    } catch {
        # Build might still be in progress
    }
}

Set-Location ".."

if (-not $buildComplete) {
    Write-Host ""
    Write-Host "[WARNING] Build still in progress after $maxAttempts checks." -ForegroundColor Yellow
    Write-Host "Check build status at:" -ForegroundColor Cyan
    Write-Host "  https://expo.dev/accounts/[your-account]/builds/$buildId" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Once build completes, download the APK manually." -ForegroundColor Yellow
    exit 0
}

if ([string]::IsNullOrWhiteSpace($downloadUrl)) {
    Write-Host "[ERROR] Could not get download URL!" -ForegroundColor Red
    Write-Host "Check: https://expo.dev/accounts/[your-account]/builds/$buildId" -ForegroundColor Yellow
    exit 1
}

# Download APK
Write-Host ""
Write-Host "Downloading APK..." -ForegroundColor Cyan
Write-Host "URL: $downloadUrl" -ForegroundColor Gray
Write-Host ""

try {
    Invoke-WebRequest -Uri $downloadUrl -OutFile $apkPath -UseBasicParsing
    
    if (Test-Path $apkPath) {
        $fileSize = (Get-Item $apkPath).Length / 1MB
        Write-Host ""
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host "  APK BUILD SUCCESSFUL!" -ForegroundColor Green
        Write-Host "============================================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "APK Location: $apkPath" -ForegroundColor Cyan
        Write-Host "File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Copy this APK to your phone and install it!" -ForegroundColor Green
        Write-Host ""
        Write-Host "The app is configured to connect to:" -ForegroundColor Yellow
        Write-Host "  $RAILWAY_URL/api/v1" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Login credentials:" -ForegroundColor Yellow
        Write-Host "  Username: admin" -ForegroundColor White
        Write-Host "  Password: admin123" -ForegroundColor White
        Write-Host ""
    } else {
        Write-Host "[ERROR] APK download failed!" -ForegroundColor Red
        Write-Host "Download manually from: $downloadUrl" -ForegroundColor Yellow
        exit 1
    }
} catch {
    Write-Host "[ERROR] Download failed: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Download manually from:" -ForegroundColor Yellow
    Write-Host "  $downloadUrl" -ForegroundColor Cyan
    exit 1
}

Write-Host "============================================================" -ForegroundColor Green
Write-Host "  COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
