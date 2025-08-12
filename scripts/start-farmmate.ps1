# FarmMate Three-Tier Architecture Startup Script (PowerShell)

Write-Host "🌾 Starting FarmMate Agricultural AI System..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
}
catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

Write-Host "🔧 Building and starting all services..." -ForegroundColor Yellow

# Build and start all services
docker-compose up --build -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep 15

# Check service health
Write-Host "🔍 Checking service health..." -ForegroundColor Cyan

Write-Host "📊 Python AI Server (port 8000):" -ForegroundColor Blue
try {
    Invoke-WebRequest -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5 | Out-Null
    Write-Host "✅ AI Server is healthy" -ForegroundColor Green
}
catch {
    Write-Host "❌ AI Server not ready yet" -ForegroundColor Red
}

Write-Host "📊 Express Gateway (port 5000):" -ForegroundColor Blue  
try {
    Invoke-WebRequest -Uri "http://localhost:5000/health" -Method GET -TimeoutSec 5 | Out-Null
    Write-Host "✅ Express Gateway is healthy" -ForegroundColor Green
}
catch {
    Write-Host "❌ Gateway not ready yet" -ForegroundColor Red
}

Write-Host "📊 React Frontend (port 3000):" -ForegroundColor Blue
try {
    Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 5 | Out-Null
    Write-Host "✅ React Frontend is healthy" -ForegroundColor Green
}
catch {
    Write-Host "❌ Frontend not ready yet" -ForegroundColor Red
}

Write-Host ""
Write-Host "🎉 FarmMate Services Started!" -ForegroundColor Green
Write-Host "🌐 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔗 Express API: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🤖 Python AI: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan

Write-Host ""
Write-Host "📋 Useful Commands:" -ForegroundColor Yellow
Write-Host "View logs: docker-compose logs -f [service-name]" -ForegroundColor White
Write-Host "Stop all: docker-compose down" -ForegroundColor White
Write-Host "Restart: docker-compose restart [service-name]" -ForegroundColor White
