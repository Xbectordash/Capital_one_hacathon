# FarmMate - Direct Build Guide (बिना Docker के)

## 🎯 Overview
यह guide Docker के बिना FarmMate services और Android app को build करने के लिए है।

## 🔧 System Requirements

### Backend Services के लिए:
- **Python 3.11+** (AI Service के लिए)
- **Node.js 18+** (Express Backend के लिए)
- **Git** (code download के लिए)

### Android App के लिए:
- **Flutter SDK 3.16+**
- **Android Studio** या **VS Code with Flutter extension**
- **Android SDK**
- **Java JDK 17+**

## 🚀 Step-by-Step Build Process

### Step 1: Python AI Service Build करें

```powershell
# Navigate to AI service directory
cd agent-python

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirement.txt

# Set environment variables
copy env\sample.env env\.env
# Edit env\.env file and add your API keys

# Test the service
python src\start_server.py
```

**Service URL**: `http://localhost:8000`
**Health Check**: `http://localhost:8000/health`

### Step 2: Express Backend Build करें

```powershell
# Open new terminal window
cd backend

# Install dependencies
npm install

# Set environment variables
$env:NODE_ENV="development"
$env:PORT="5000"
$env:PYTHON_SERVER_URL="ws://localhost:8000"

# Start the backend
npm start
```

**Service URL**: `http://localhost:5000`
**Health Check**: `http://localhost:5000/health`

### Step 3: Android App Build करें

```powershell
# Open new terminal window
cd frontend\android-app\farmmate

# Get Flutter dependencies
flutter pub get

# Run in development mode (localhost services)
flutter run

# OR build APK for testing
flutter build apk --debug

# OR build production APK (for local services)
flutter build apk --release --dart-define=DEBUG_MODE=true
```

## 📱 Android App Development Build

### Quick Development Setup:
```powershell
# Start all services in different terminal windows

# Terminal 1: Python AI Service
cd agent-python
.\venv\Scripts\Activate.ps1
python src\start_server.py

# Terminal 2: Express Backend  
cd backend
npm start

# Terminal 3: Android App
cd frontend\android-app\farmmate
flutter run
```

### Build APK for Local Testing:
```powershell
cd frontend\android-app\farmmate

# Clean previous builds
flutter clean
flutter pub get

# Build debug APK (for testing with localhost)
flutter build apk --debug

# Install on connected device
adb install build\app\outputs\flutter-apk\app-debug.apk
```

## 🌐 Production Build (Without Docker)

### For Deployed Services:

#### 1. Update Android App Configuration
```dart
// In lib\config\production_config.dart
static const String backendUrl = 'https://your-backend-url.com';
static const String aiServiceUrl = 'https://your-ai-service-url.com';
```

#### 2. Build Production APK
```powershell
cd frontend\android-app\farmmate

flutter build apk --release --dart-define=DEBUG_MODE=false
```

## 🔧 Manual Deployment (Without Docker)

### Python AI Service:
```powershell
# For Render.com manual deployment
# 1. Create new Web Service
# 2. Connect GitHub repo
# 3. Set build command: pip install -r requirement.txt
# 4. Set start command: python src/start_server.py
# 5. Set environment variables in dashboard
```

### Express Backend:
```powershell
# For Render.com manual deployment  
# 1. Create new Web Service
# 2. Connect GitHub repo  
# 3. Set build command: npm install
# 4. Set start command: npm start
# 5. Set environment variables in dashboard
```

## 🧪 Testing Without Docker

### Test Python AI Service:
```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test chat endpoint
$body = @{
    user_id = "test_user"
    message = "Hello"
    language = "hi"
    location = "India"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method POST -Body $body -ContentType "application/json"
```

### Test Express Backend:
```powershell
# Test health endpoint
curl http://localhost:5000/health

# Test chat endpoint
$body = @{
    user_id = "test_user"
    message = "Hello"
    language = "hi"
    location = "India"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/chat" -Method POST -Body $body -ContentType "application/json"
```

### Test Android App:
```powershell
# Run on emulator
flutter run

# Or install APK on physical device
adb install build\app\outputs\flutter-apk\app-debug.apk
```

## 🔍 Troubleshooting

### Common Issues:

#### 1. Python Dependencies Error:
```powershell
# Solution: Update pip and reinstall
python -m pip install --upgrade pip
pip install -r requirement.txt --force-reinstall
```

#### 2. Node.js Modules Error:
```powershell
# Solution: Clear cache and reinstall
npm cache clean --force
rm -rf node_modules
npm install
```

#### 3. Flutter Build Error:
```powershell
# Solution: Clean and rebuild
flutter clean
flutter pub get
flutter doctor  # Check for issues
```

#### 4. Android SDK Issues:
```powershell
# Solution: Accept licenses
flutter doctor --android-licenses
```

## 📊 Build Time Comparison

| Method | Python AI | Express Backend | Android App | Total Time |
|--------|-----------|-----------------|-------------|------------|
| **Direct Build** | 2-3 min | 1-2 min | 3-5 min | **6-10 min** |
| **Docker Build** | 5-8 min | 3-5 min | N/A | **8-13 min** |

## 💡 Pro Tips

### 1. Development Workflow:
```powershell
# Use these for faster development cycles
# Terminal 1: Python service with auto-reload
cd agent-python
.\venv\Scripts\Activate.ps1
python -m uvicorn src.server.app:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Express with nodemon
cd backend
npm run dev  # Uses nodemon for auto-restart

# Terminal 3: Flutter hot reload
cd frontend\android-app\farmmate
flutter run  # Hot reload on code changes
```

### 2. Quick Build Script:
```powershell
# Create build_local.ps1 in project root
# This builds everything locally without Docker

# Start Python AI Service
Start-Process powershell -ArgumentList "-Command", "cd agent-python; .\venv\Scripts\Activate.ps1; python src\start_server.py" -WindowStyle Normal

# Wait 10 seconds for AI service to start
Start-Sleep -Seconds 10

# Start Express Backend
Start-Process powershell -ArgumentList "-Command", "cd backend; npm start" -WindowStyle Normal

# Wait 5 seconds for backend to start  
Start-Sleep -Seconds 5

# Build Android APK
cd frontend\android-app\farmmate
flutter build apk --debug

Write-Host "✅ All services started and APK built!" -ForegroundColor Green
```

## 🎉 Advantages of Direct Build

✅ **Faster Build Times** - No Docker overhead  
✅ **Easier Debugging** - Direct access to logs  
✅ **Hot Reload** - Faster development cycles  
✅ **Native Performance** - No containerization overhead  
✅ **Simple Deployment** - Direct to cloud platforms  
✅ **Resource Efficient** - Uses less RAM/CPU  

## 🚀 Ready to Build!

Direct build approach है perfect for:
- **Development और Testing**
- **Quick prototyping** 
- **Local debugging**
- **Performance optimization**

बस follow करें steps और आपका FarmMate app ready हो जाएगा! 🎯
