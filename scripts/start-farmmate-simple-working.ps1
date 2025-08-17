# Simple FarmMate Local Development Startup Script
# This matches your Render/Vercel cloud deployment setup locally

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "cleanup")]
    [string]$Command = "start"
)

Write-Host "🌾 FarmMate Simple Local Development Setup" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Yellow

function Test-Docker {
    try {
        docker --version | Out-Null
        Write-Host "✅ Docker is available" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
        return $false
    }
}

function Test-Ports {
    $ports = @(3000, 5000, 8000)
    $unavailable = @()
    
    foreach ($port in $ports) {
        try {
            $connection = Test-NetConnection -ComputerName "localhost" -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
            if ($connection) {
                $unavailable += $port
            }
        } catch {
            # Port is available
        }
    }
    
    if ($unavailable.Count -gt 0) {
        Write-Host "❌ Ports in use: $($unavailable -join ', ')" -ForegroundColor Red
        Write-Host "   Please stop services using these ports" -ForegroundColor Yellow
        return $false
    }
    
    Write-Host "✅ Ports 3000, 5000, 8000 are available" -ForegroundColor Green
    return $true
}

function Start-Services {
    Write-Host "🚀 Starting FarmMate services..." -ForegroundColor Blue
    
    # Build and start with the simple docker-compose.yml
    docker-compose -f docker-compose.yml build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to build services" -ForegroundColor Red
        exit 1
    }
    
    docker-compose -f docker-compose.yml up -d
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to start services" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
    
    # Check if services are running
    $containers = docker-compose -f docker-compose.yml ps --services --filter "status=running"
    
    Write-Host "✅ Services started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔗 Access your application:" -ForegroundColor Blue
    Write-Host "   🌾 Frontend (React):     http://localhost:3000" -ForegroundColor Green
    Write-Host "   🚀 Backend (Express):    http://localhost:5000" -ForegroundColor Green
    Write-Host "   🐍 AI Service (Python):  http://localhost:8000" -ForegroundColor Green
    Write-Host ""
    
    # Open the frontend in browser
    Start-Process "http://localhost:3000"
}

function Stop-Services {
    Write-Host "🛑 Stopping FarmMate services..." -ForegroundColor Yellow
    docker-compose -f docker-compose.yml down
    Write-Host "✅ All services stopped" -ForegroundColor Green
}

function Show-Status {
    Write-Host "📊 FarmMate Service Status:" -ForegroundColor Blue
    docker-compose -f docker-compose.yml ps
    
    Write-Host ""
    Write-Host "🔗 Service URLs:" -ForegroundColor Blue
    Write-Host "   🌾 Frontend: http://localhost:3000" -ForegroundColor Green
    Write-Host "   🚀 Backend:  http://localhost:5000" -ForegroundColor Green  
    Write-Host "   🐍 AI Service: http://localhost:8000" -ForegroundColor Green
}

function Show-Logs {
    Write-Host "📋 Showing logs for all services..." -ForegroundColor Blue
    docker-compose -f docker-compose.yml logs -f
}

function Cleanup-Services {
    Write-Host "🧹 Cleaning up Docker resources..." -ForegroundColor Yellow
    docker-compose -f docker-compose.yml down -v --remove-orphans
    docker system prune -f
    Write-Host "✅ Cleanup completed" -ForegroundColor Green
}

# Main execution
switch ($Command) {
    "start" {
        if (-not (Test-Docker)) { exit 1 }
        if (-not (Test-Ports)) { exit 1 }
        Start-Services
    }
    
    "stop" {
        Stop-Services
    }
    
    "restart" {
        Stop-Services
        Start-Sleep -Seconds 2
        if (Test-Docker -and Test-Ports) {
            Start-Services
        }
    }
    
    "status" {
        Show-Status
    }
    
    "logs" {
        Show-Logs
    }
    
    "cleanup" {
        Cleanup-Services
    }
    
    default {
        Write-Host "🌾 FarmMate Simple Development Script" -ForegroundColor Blue
        Write-Host ""
        Write-Host "Usage: .\start-farmmate-simple-working.ps1 [command]" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Commands:"
        Write-Host "  start    - Start all services (default)"
        Write-Host "  stop     - Stop all services"
        Write-Host "  restart  - Restart all services"
        Write-Host "  status   - Show service status"
        Write-Host "  logs     - Show logs for all services"
        Write-Host "  cleanup  - Stop services and clean up"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  .\start-farmmate-simple-working.ps1 start"
        Write-Host "  .\start-farmmate-simple-working.ps1 logs"
    }
}
