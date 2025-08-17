# Ultra Simple FarmMate Startup - Just the basics!
# This script simply starts your 3 services locally to match Render/Vercel deployment

Write-Host "🌾 FarmMate - Ultra Simple Local Startup" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "ℹ️  This script starts FarmMate locally using Docker" -ForegroundColor Blue
Write-Host "   (Just like how it runs on Render/Vercel but on your machine)" -ForegroundColor Gray
Write-Host ""

# Check what's currently running
Write-Host "🔍 Checking current services..." -ForegroundColor Yellow
docker-compose -f docker-compose.yml ps

Write-Host ""
Write-Host "🚀 Starting FarmMate services..." -ForegroundColor Blue
Write-Host "   Building and starting: AI Server, Backend, Frontend" -ForegroundColor Gray

# Simple start command
docker-compose -f docker-compose.yml up --build -d

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ FarmMate started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Your application is now running at:" -ForegroundColor Blue
    Write-Host "   🌾 Web App:     http://localhost:3000  (Click to test!)" -ForegroundColor Green
    Write-Host "   🚀 Backend:     http://localhost:5000" -ForegroundColor Yellow  
    Write-Host "   🐍 AI Service:  http://localhost:8000" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "💡 Quick Commands:" -ForegroundColor Blue
    Write-Host "   Stop all:       docker-compose -f docker-compose.yml down" -ForegroundColor Gray
    Write-Host "   View logs:      docker-compose -f docker-compose.yml logs -f" -ForegroundColor Gray
    Write-Host "   Restart:        docker-compose -f docker-compose.yml restart" -ForegroundColor Gray
    Write-Host ""
    
    # Wait a bit then open browser
    Write-Host "🌐 Opening web app in 5 seconds..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
    Start-Process "http://localhost:3000"
    
} else {
    Write-Host ""
    Write-Host "❌ Failed to start FarmMate" -ForegroundColor Red
    Write-Host "💡 Try stopping existing services first:" -ForegroundColor Yellow
    Write-Host "   docker-compose -f docker-compose.yml down" -ForegroundColor Gray
    Write-Host "   Then run this script again" -ForegroundColor Gray
}

Write-Host ""
Write-Host "📝 Note: This is the same setup as your Render/Vercel deployment" -ForegroundColor Blue
Write-Host "   but running locally for development and testing" -ForegroundColor Gray
