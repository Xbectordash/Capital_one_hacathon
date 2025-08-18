# Simple APK Build Script - Environment Variable Based
# यह script .env file या command line arguments के base पर APK build करता है

Write-Host "🚀 FarmMate APK Builder (Environment Based)" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "frontend\android-app\farmmate\pubspec.yaml")) {
    Write-Host "❌ Error: Run this script from project root directory" -ForegroundColor Red
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
Write-Host "1. Build with .env file settings (Cloud Services)"
Write-Host "2. Build with custom URLs"
Write-Host "3. Build for local development"

$choice = Read-Host "Choose option (1-3)"

cd frontend\android-app\farmmate

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🌐 Building with .env configuration..." -ForegroundColor Green
        Write-Host "   Backend: https://capital-one-hacathon-1.onrender.com" -ForegroundColor Cyan
        Write-Host "   AI Service: https://capital-one-hacathon.onrender.com" -ForegroundColor Cyan
        
        Write-Host ""
        Write-Host "📱 Building APK..." -ForegroundColor Blue
        flutter pub get
        flutter clean
        flutter pub get
        flutter build apk --release
    }
    
    "2" {
        Write-Host ""
        $backendUrl = Read-Host "Enter Backend URL (e.g., https://your-backend.com)"
        $aiUrl = Read-Host "Enter AI Service URL (e.g., https://your-ai.com)"
        
        Write-Host ""
        Write-Host "🌐 Building with custom URLs..." -ForegroundColor Green
        Write-Host "   Backend: $backendUrl" -ForegroundColor Cyan
        Write-Host "   AI Service: $aiUrl" -ForegroundColor Cyan
        
        Write-Host ""
        Write-Host "📱 Building APK..." -ForegroundColor Blue
        flutter pub get
        flutter clean
        flutter pub get
        flutter build apk --release --dart-define=BACKEND_URL=$backendUrl --dart-define=AI_SERVICE_URL=$aiUrl --dart-define=DEBUG_MODE=false
    }
    
    "3" {
        Write-Host ""
        Write-Host "🏠 Building for local development..." -ForegroundColor Green
        Write-Host "   Backend: http://10.0.2.2:5000" -ForegroundColor Cyan
        Write-Host "   AI Service: http://10.0.2.2:8000" -ForegroundColor Cyan
        
        Write-Host ""
        Write-Host "📱 Building APK..." -ForegroundColor Blue
        flutter pub get
        flutter clean
        flutter pub get
        flutter build apk --debug --dart-define=BACKEND_URL=http://10.0.2.2:5000 --dart-define=AI_SERVICE_URL=http://10.0.2.2:8000 --dart-define=DEBUG_MODE=true
    }
    
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
        exit 1
    }
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ APK Build Successful!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 APK Location:" -ForegroundColor Cyan
    if ($choice -eq "3") {
        Write-Host "   build\app\outputs\flutter-apk\app-debug.apk"
    } else {
        Write-Host "   build\app\outputs\flutter-apk\app-release.apk"
    }
    Write-Host ""
    Write-Host "📲 Install APK:" -ForegroundColor Yellow
    if ($choice -eq "3") {
        Write-Host "   adb install build\app\outputs\flutter-apk\app-debug.apk"
    } else {
        Write-Host "   adb install build\app\outputs\flutter-apk\app-release.apk"
    }
    Write-Host ""
    
    # Check if device is connected
    try {
        $devices = adb devices 2>$null
        if ($devices -match "device$") {
            Write-Host "📱 Device detected! Install now?" -ForegroundColor Yellow
            $install = Read-Host "Press 'y' to install APK on device (y/N)"
            if ($install -match '^[Yy]$') {
                Write-Host "Installing APK..." -ForegroundColor Blue
                if ($choice -eq "3") {
                    adb install -r build\app\outputs\flutter-apk\app-debug.apk
                } else {
                    adb install -r build\app\outputs\flutter-apk\app-release.apk
                }
                Write-Host "✅ APK installed successfully!" -ForegroundColor Green
            }
        }
    } catch {
        Write-Host "ℹ️  No device connected or ADB not found" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "❌ APK Build Failed!" -ForegroundColor Red
    Write-Host "Check the error messages above" -ForegroundColor Yellow
}

cd ..\..\..
Write-Host ""
Write-Host "🎉 Done!" -ForegroundColor Green
