# FarmMate - Quick Start Script (Development)
# यह script सभी services को development mode में start करता है

Write-Host "🔥 FarmMate Quick Start (Development Mode)" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "यह script सभी services को development mode में start करेगा" -ForegroundColor Yellow
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "agent-python") -or -not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "🔍 Checking Services..." -ForegroundColor Green

# Check Python environment
if (-not (Test-Path "agent-python\venv")) {
    Write-Host "⚠️  Python virtual environment not found. Creating..." -ForegroundColor Yellow
    cd agent-python
    python -m venv venv
    & .\venv\Scripts\Activate.ps1
    pip install -r requirement.txt
    cd ..
    Write-Host "✅ Python environment created!" -ForegroundColor Green
}

# Check Node modules
if (-not (Test-Path "backend\node_modules")) {
    Write-Host "⚠️  Node modules not found. Installing..." -ForegroundColor Yellow
    cd backend
    npm install
    cd ..
    Write-Host "✅ Node modules installed!" -ForegroundColor Green
}

# Check Flutter dependencies
cd frontend\android-app\farmmate
if (-not (Test-Path ".packages") -and -not (Test-Path ".dart_tool")) {
    Write-Host "⚠️  Flutter dependencies not found. Getting..." -ForegroundColor Yellow
    flutter pub get
    Write-Host "✅ Flutter dependencies ready!" -ForegroundColor Green
}
cd ..\..\..

Write-Host ""
Write-Host "🚀 Starting All Services..." -ForegroundColor Cyan
Write-Host ""

# Start Python AI Service
Write-Host "🐍 Starting Python AI Service..." -ForegroundColor Yellow
$pythonJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    cd agent-python; 
    .\venv\Scripts\Activate.ps1; 
    Write-Host '🐍 Python AI Service Starting...' -ForegroundColor Green;
    Write-Host '📡 URL: http://localhost:8000' -ForegroundColor Cyan;
    Write-Host '❤️  Health: http://localhost:8000/health' -ForegroundColor Cyan;
    Write-Host '📚 Docs: http://localhost:8000/docs' -ForegroundColor Cyan;
    Write-Host '';
    python src\start_server.py
" -WindowStyle Normal -PassThru

# Wait for Python service to start
Write-Host "⏳ Waiting for Python AI Service to start..." -ForegroundColor Blue
Start-Sleep -Seconds 10

# Start Express Backend
Write-Host "🌐 Starting Express Backend..." -ForegroundColor Yellow
$nodeJob = Start-Process powershell -ArgumentList "-NoExit", "-Command", "
    cd backend; 
    Write-Host '🌐 Express Backend Starting...' -ForegroundColor Green;
    Write-Host '📡 URL: http://localhost:5000' -ForegroundColor Cyan;
    Write-Host '❤️  Health: http://localhost:5000/health' -ForegroundColor Cyan;
    Write-Host '🔌 WebSocket: ws://localhost:5000' -ForegroundColor Cyan;
    Write-Host '';
    npm start
" -WindowStyle Normal -PassThru

# Wait for Express service to start
Write-Host "⏳ Waiting for Express Backend to start..." -ForegroundColor Blue
Start-Sleep -Seconds 8

# Test services
Write-Host "🧪 Testing Services..." -ForegroundColor Green

try {
    $pythonHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "✅ Python AI Service: Running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Python AI Service: Not responding yet" -ForegroundColor Yellow
}

try {
    $nodeHealth = Invoke-RestMethod -Uri "http://localhost:5000/health" -TimeoutSec 5
    Write-Host "✅ Express Backend: Running" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Express Backend: Not responding yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📱 Flutter App Options:" -ForegroundColor Cyan
Write-Host "1. Run on emulator/device (flutter run)"
Write-Host "2. Build debug APK"
Write-Host "3. Skip Flutter for now"

$flutterChoice = Read-Host "Choose option (1-3)"

switch ($flutterChoice) {
    "1" {
        Write-Host "📱 Starting Flutter App..." -ForegroundColor Yellow
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "
            cd frontend\android-app\farmmate; 
            Write-Host '📱 Flutter App Starting...' -ForegroundColor Green;
            Write-Host '🔗 Connecting to localhost services' -ForegroundColor Cyan;
            Write-Host '';
            flutter run
        " -WindowStyle Normal
    }
    
    "2" {
        Write-Host "🔨 Building Flutter APK..." -ForegroundColor Yellow
        cd frontend\android-app\farmmate
        flutter build apk --debug
        Write-Host "✅ APK built: build\app\outputs\flutter-apk\app-debug.apk" -ForegroundColor Green
        Write-Host "📲 Install with: adb install build\app\outputs\flutter-apk\app-debug.apk" -ForegroundColor Cyan
        cd ..\..\..
    }
    
    "3" {
        Write-Host "⏭️  Skipping Flutter app" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "🎉 Development Environment Ready!" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Service URLs:" -ForegroundColor Cyan
Write-Host "   🐍 Python AI Service:  http://localhost:8000"
Write-Host "   🌐 Express Backend:     http://localhost:5000"
Write-Host "   📚 API Documentation:   http://localhost:8000/docs"
Write-Host "   🧪 Test Page:           http://localhost:8000/test-page"
Write-Host ""
Write-Host "🧪 Quick Tests:" -ForegroundColor Yellow
Write-Host "   curl http://localhost:8000/health"
Write-Host "   curl http://localhost:5000/health"
Write-Host ""
Write-Host "📱 Flutter Commands:" -ForegroundColor Yellow
Write-Host "   cd frontend\android-app\farmmate"
Write-Host "   flutter run                    # Run on device"
Write-Host "   flutter build apk --debug      # Build APK"
Write-Host ""
Write-Host "⛔ To stop services:" -ForegroundColor Red
Write-Host "   Close the PowerShell windows or press Ctrl+C in each"
Write-Host ""

# Keep script running and show monitoring
Write-Host "🔍 Service Monitor (Press 'q' to quit, 'r' to refresh)" -ForegroundColor Cyan

do {
    Write-Host "`n--- Service Status ---" -ForegroundColor Blue
    
    # Check Python service
    try {
        $pythonHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 2
        Write-Host "🐍 Python AI Service: ✅ Running" -ForegroundColor Green
    } catch {
        Write-Host "🐍 Python AI Service: ❌ Down" -ForegroundColor Red
    }
    
    # Check Express service
    try {
        $nodeHealth = Invoke-RestMethod -Uri "http://localhost:5000/health" -TimeoutSec 2
        Write-Host "🌐 Express Backend: ✅ Running" -ForegroundColor Green
    } catch {
        Write-Host "🌐 Express Backend: ❌ Down" -ForegroundColor Red
    }
    
    Write-Host "`nPress 'q' to quit, 'r' to refresh, or wait 30 seconds..." -ForegroundColor Yellow
    
    $timeout = 30
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    
    while ($timer.Elapsed.TotalSeconds -lt $timeout) {
        if ($Host.UI.RawUI.KeyAvailable) {
            $key = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            if ($key.Character -eq 'q' -or $key.Character -eq 'Q') {
                Write-Host "`n👋 Exiting monitor..." -ForegroundColor Yellow
                return
            } elseif ($key.Character -eq 'r' -or $key.Character -eq 'R') {
                Write-Host "`n🔄 Refreshing..." -ForegroundColor Blue
                break
            }
        }
        Start-Sleep -Milliseconds 100
    }
    
    $timer.Stop()
    
} while ($true)
