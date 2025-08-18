# FarmMate - Quick Build Script (बिना Docker के)
# यह script सभी services को locally build और start करता है

Write-Host "🚀 FarmMate Local Build Script (Without Docker)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "यह script Docker के बिना सभी services build करेगा" -ForegroundColor Yellow
Write-Host ""

# Check prerequisites
Write-Host "🔍 Checking Prerequisites..." -ForegroundColor Green

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
try {
    $nodeVersion = node --version
    Write-Host "✅ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found. Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Check Flutter
try {
    $flutterVersion = flutter --version | Select-Object -First 1
    Write-Host "✅ Flutter: $flutterVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Flutter not found. Please install Flutter SDK" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "📋 Build Options:" -ForegroundColor Yellow
Write-Host "1. Build Android APK (connects to deployed services)"
Write-Host "2. Build केवल Python AI Service"
Write-Host "3. Build केवल Express Backend"
Write-Host "4. Start Development Servers (All services)"

$choice = Read-Host "Choose option (1-4)"

switch ($choice) {
    "1" {
        Write-Host "🔨 Building Android APK..." -ForegroundColor Cyan
        
        # Build Android APK
        Write-Host ""
        Write-Host "📱 Building Android APK (DEPLOYED services)..." -ForegroundColor Yellow
        cd frontend\android-app\farmmate
        
        Write-Host "Getting Flutter dependencies..." -ForegroundColor Blue
        flutter pub get
        
        Write-Host "Building production APK for deployed services..." -ForegroundColor Blue
        flutter build apk --release
        
        Write-Host "✅ Android APK ready!" -ForegroundColor Green
        Write-Host "📁 APK Location: build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor Cyan
        Write-Host "🌐 URLs: https://capital-one-hacathon-1.onrender.com" -ForegroundColor Yellow
    }
    
    "2" {
        Write-Host "🐍 Building Python AI Service Only..." -ForegroundColor Cyan
        cd agent-python
        
        if (-not (Test-Path "venv")) {
            python -m venv venv
        }
        
        & .\venv\Scripts\Activate.ps1
        pip install -r requirement.txt
        
        Write-Host "✅ Python AI Service ready!" -ForegroundColor Green
        Write-Host "🚀 To start: cd agent-python && .\venv\Scripts\Activate.ps1 && python src\start_server.py" -ForegroundColor Cyan
    }
    
    "3" {
        Write-Host "🌐 Building Express Backend Only..." -ForegroundColor Cyan
        cd backend
        
        npm install
        
        Write-Host "✅ Express Backend ready!" -ForegroundColor Green
        Write-Host "🚀 To start: cd backend && npm start" -ForegroundColor Cyan
    }
    
    "4" {
        Write-Host "🚀 Starting Development Servers..." -ForegroundColor Cyan
        
        # Start Python AI Service
        Write-Host "Starting Python AI Service..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd agent-python; .\venv\Scripts\Activate.ps1; Write-Host 'Python AI Service starting...' -ForegroundColor Green; python src\start_server.py" -WindowStyle Normal
        
        Start-Sleep -Seconds 8
        
        # Start Express Backend
        Write-Host "Starting Express Backend..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; Write-Host 'Express Backend starting...' -ForegroundColor Green; npm start" -WindowStyle Normal
        
        Start-Sleep -Seconds 5
        
        # Start Flutter App
        Write-Host "Starting Flutter App..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend\android-app\farmmate; Write-Host 'Flutter App starting...' -ForegroundColor Green; flutter run" -WindowStyle Normal
        
        Write-Host ""
        Write-Host "✅ All services started!" -ForegroundColor Green
        Write-Host "🌐 Python AI Service: http://localhost:8000" -ForegroundColor Cyan
        Write-Host "🌐 Express Backend: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "📱 Flutter App: Running on connected device/emulator" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Yellow
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        return
    }
    
    default {
        Write-Host "❌ Invalid option selected" -ForegroundColor Red
        exit 1
    }
}

Write-Host ""
Write-Host "🎉 Build Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "🧪 Testing URLs:" -ForegroundColor Cyan
Write-Host "   Python AI Service: http://localhost:8000/health"
Write-Host "   Express Backend: http://localhost:5000/health"
Write-Host ""
Write-Host "📱 Android APK Installation:" -ForegroundColor Cyan
Write-Host "   adb install build\app\outputs\flutter-apk\app-debug.apk"
Write-Host ""
Write-Host "🚀 To start services manually:" -ForegroundColor Yellow
Write-Host "   Python AI: cd agent-python && .\venv\Scripts\Activate.ps1 && python src\start_server.py"
Write-Host "   Express: cd backend && npm start"
Write-Host "   Flutter: cd frontend\android-app\farmmate && flutter run"
