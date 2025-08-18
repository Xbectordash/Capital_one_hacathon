# FarmMate Android App - Production Build Script (PowerShell)
# This script builds the Android app for production deployment

Write-Host "🚀 FarmMate Android Production Build Script" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan

# Check if we're in the right directory
if (-not (Test-Path "pubspec.yaml")) {
    Write-Host "❌ Error: pubspec.yaml not found. Run this script from the farmmate flutter project root." -ForegroundColor Red
    exit 1
}

# Check if Flutter is installed
try {
    flutter --version | Out-Null
} catch {
    Write-Host "❌ Error: Flutter not found. Please install Flutter and add it to PATH." -ForegroundColor Red
    exit 1
}

Write-Host "📋 Pre-build Checklist" -ForegroundColor Yellow
Write-Host "=====================" -ForegroundColor Yellow
Write-Host "✅ Make sure backend services are deployed"
Write-Host "✅ Update URLs in lib/config/production_config.dart"
Write-Host "✅ Test services are responding to health checks"
Write-Host ""

$response = Read-Host "Have you completed the checklist above? (y/N)"
if ($response -notmatch '^[Yy]$') {
    Write-Host "❌ Please complete the checklist before building for production." -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Validating Flutter setup..." -ForegroundColor Green
flutter doctor

Write-Host "📦 Getting dependencies..." -ForegroundColor Green
flutter pub get

Write-Host "🔧 Running code generation..." -ForegroundColor Green
if ((Test-Path "build_runner.yaml") -or (Get-Content "pubspec.yaml" | Select-String "build_runner")) {
    flutter packages pub run build_runner build --delete-conflicting-outputs
}

Write-Host "🧹 Cleaning previous builds..." -ForegroundColor Green
flutter clean
flutter pub get

Write-Host "🔨 Building production APK..." -ForegroundColor Green
Write-Host "Building with production configuration (DEBUG_MODE=false)..." -ForegroundColor Yellow

# Build APK for production
flutter build apk `
    --dart-define=DEBUG_MODE=false `
    --dart-define=BACKEND_URL=https://farmmate-backend.onrender.com `
    --dart-define=AI_SERVICE_URL=https://farmmate-ai-server.onrender.com `
    --target-platform android-arm,android-arm64,android-x64 `
    --split-per-abi

Write-Host "📱 Building App Bundle for Play Store..." -ForegroundColor Green
flutter build appbundle `
    --dart-define=DEBUG_MODE=false `
    --dart-define=BACKEND_URL=https://farmmate-backend.onrender.com `
    --dart-define=AI_SERVICE_URL=https://farmmate-ai-server.onrender.com

Write-Host "✅ Build completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📁 Build artifacts:" -ForegroundColor Cyan
Write-Host "   APK (Universal): build/app/outputs/flutter-apk/app-release.apk"
Write-Host "   APK (Split):     build/app/outputs/flutter-apk/app-*-release.apk"
Write-Host "   App Bundle:      build/app/outputs/bundle/release/app-release.aab"
Write-Host ""

# Check if ADB is available for installation
try {
    adb version | Out-Null
    Write-Host "📲 Install options:" -ForegroundColor Cyan
    Write-Host "   adb install build/app/outputs/flutter-apk/app-release.apk"
    Write-Host ""
    
    $installResponse = Read-Host "Install APK on connected device now? (y/N)"
    if ($installResponse -match '^[Yy]$') {
        Write-Host "📲 Installing APK..." -ForegroundColor Green
        adb install -r build/app/outputs/flutter-apk/app-release.apk
        Write-Host "✅ Installation completed!" -ForegroundColor Green
        
        Write-Host ""
        Write-Host "🧪 Testing suggestions:" -ForegroundColor Yellow
        Write-Host "   1. Open the app and check Settings > Service Status"
        Write-Host "   2. Test chat functionality with deployed backend"
        Write-Host "   3. Verify location services work"
        Write-Host "   4. Test file upload functionality"
    }
} catch {
    Write-Host "ℹ️  ADB not found. You can manually install the APK later." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Test the APK thoroughly on devices"
Write-Host "   2. Verify all services are working"
Write-Host "   3. Share APK or upload App Bundle to Play Console"
Write-Host ""
Write-Host "🎉 Production build ready for deployment!" -ForegroundColor Green
