# Enhanced Docker Startup Script for FarmMate with Monitoring (PowerShell)
# This script manages the complete Docker-based deployment on Windows

param(
    [Parameter(Position=0)]
    [ValidateSet("start", "dev", "stop", "restart", "status", "logs", "cleanup", "backup", "restore", "update", "build", "shell")]
    [string]$Command = "start",
    
    [Parameter(Position=1)]
    [string]$ServiceName,
    
    [switch]$SkipPortCheck
)

# Configuration
$ComposeFile = "docker-compose.yml"
$DevComposeFile = "docker-compose.yml"  # Using same file for now, can create dev version later
$ProjectName = "farmmate"

# Colors for output
$colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Blue"
    Purple = "Magenta"
    Cyan = "Cyan"
    White = "White"
}

# ASCII Art Banner
Write-Host "
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🐳 FARMMATE DOCKER DEPLOYMENT 🐳                         ║
║                     Three-Tier Architecture Deployment                       ║
║                                                                              ║
║   Python AI Server (Port 8000)                                               ║
║  🚀 Express Backend (Port 5000)                                             ║
║  ⚛️  React Frontend (Port 3000)                                              ║
║  🗄️  ChromaDB (Port 8001)                                                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor $colors.Cyan

# Function to check if Docker is running
function Test-Docker {
    try {
        $null = docker info 2>$null
        $dockerVersion = docker --version
        Write-Host "✅ Docker is running: $dockerVersion" -ForegroundColor $colors.Green
    } catch {
        Write-Host "❌ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor $colors.Red
        exit 1
    }
    
    try {
        $composeVersion = docker-compose --version
        Write-Host "✅ Docker Compose is available: $composeVersion" -ForegroundColor $colors.Green
    } catch {
        Write-Host "❌ Docker Compose is not available. Please install docker-compose." -ForegroundColor $colors.Red
        exit 1
    }
}

# Function to check if ports are available
function Test-Ports {
    $ports = @(8000, 5000, 3000, 8001)  # AI Server, Backend, Frontend, ChromaDB
    $unavailablePorts = @()
    
    foreach ($port in $ports) {
        try {
            $connection = Test-NetConnection -ComputerName "localhost" -Port $port -InformationLevel Quiet -WarningAction SilentlyContinue
            if ($connection) {
                $unavailablePorts += $port
            }
        } catch {
            # Port is available
        }
    }
    
    if ($unavailablePorts.Count -gt 0) {
        Write-Host "❌ The following ports are already in use: $($unavailablePorts -join ', ')" -ForegroundColor $colors.Red
        Write-Host "   Please stop the services using these ports or use different ports" -ForegroundColor $colors.Yellow
        return $false
    } else {
        Write-Host "✅ All required ports are available" -ForegroundColor $colors.Green
        return $true
    }
}

# Function to build and start services
function Start-Services {
    param(
        [string]$Mode = "production"
    )
    
    $composeFiles = "-f $ComposeFile"
    
    if ($Mode -eq "dev") {
        $composeFiles += " -f $DevComposeFile"
        Write-Host "🔧 Starting in development mode with file watching" -ForegroundColor $colors.Yellow
    } else {
        Write-Host "🚀 Starting in production mode" -ForegroundColor $colors.Blue
    }
    
    Write-Host "📦 Building Docker images..." -ForegroundColor $colors.Purple
    $buildCommand = "docker-compose $composeFiles -p $ProjectName build --parallel"
    Invoke-Expression $buildCommand
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to build Docker images" -ForegroundColor $colors.Red
        exit 1
    }
    
    Write-Host "🚀 Starting services..." -ForegroundColor $colors.Purple
    $startCommand = "docker-compose $composeFiles -p $ProjectName up -d"
    Invoke-Expression $startCommand
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to start services" -ForegroundColor $colors.Red
        exit 1
    }
    
    # Wait for services to start
    Write-Host "⏳ Waiting for services to start..." -ForegroundColor $colors.Yellow
    Start-Sleep -Seconds 10
    
    # Check service health
    Test-ServiceHealth
}

# Function to check service health
function Test-ServiceHealth {
    $services = @(
        @{Name="agent-python"; Port=8000; Path="/health"},
        @{Name="backend"; Port=5000; Path="/health"},
        @{Name="frontend-web"; Port=3000; Path="/"}
    )
    
    Write-Host "🔍 Checking service health..." -ForegroundColor $colors.Blue
    
    foreach ($service in $services) {
        $url = "http://localhost:$($service.Port)$($service.Path)"
        $maxAttempts = 30
        $attempt = 1
        $healthy = $false
        
        while ($attempt -le $maxAttempts -and -not $healthy) {
            try {
                $response = Invoke-WebRequest -Uri $url -TimeoutSec 5 -UseBasicParsing -DisableKeepAlive
                if ($response.StatusCode -eq 200) {
                    Write-Host "✅ $($service.Name) is healthy" -ForegroundColor $colors.Green
                    $healthy = $true
                }
            } catch {
                if ($attempt -eq $maxAttempts) {
                    Write-Host "❌ $($service.Name) failed to start (timeout after $maxAttempts attempts)" -ForegroundColor $colors.Red
                    Write-Host "   Check logs: docker-compose -p $ProjectName logs $($service.Name)" -ForegroundColor $colors.Yellow
                } else {
                    Write-Host "⏳ Waiting for $($service.Name)... (attempt $attempt/$maxAttempts)" -ForegroundColor $colors.Yellow
                    Start-Sleep -Seconds 2
                    $attempt++
                }
            }
        }
    }
}

# Function to stop services
function Stop-Services {
    Write-Host "🛑 Stopping FarmMate services..." -ForegroundColor $colors.Yellow
    $stopCommand = "docker-compose -f $ComposeFile -p $ProjectName down"
    Invoke-Expression $stopCommand
    Write-Host "✅ All services stopped" -ForegroundColor $colors.Green
}

# Function to clean up
function Invoke-Cleanup {
    Write-Host "🧹 Cleaning up Docker resources..." -ForegroundColor $colors.Yellow
    $cleanupCommand = "docker-compose -f $ComposeFile -p $ProjectName down -v --remove-orphans"
    Invoke-Expression $cleanupCommand
    docker system prune -f
    Write-Host "✅ Cleanup completed" -ForegroundColor $colors.Green
}

# Function to show logs
function Show-Logs {
    param([string]$ServiceName)
    
    if ([string]::IsNullOrEmpty($ServiceName)) {
        $logsCommand = "docker-compose -f $ComposeFile -p $ProjectName logs -f"
    } else {
        $logsCommand = "docker-compose -f $ComposeFile -p $ProjectName logs -f $ServiceName"
    }
    Invoke-Expression $logsCommand
}

# Function to show status
function Show-Status {
    Write-Host "📊 FarmMate Service Status:" -ForegroundColor $colors.Blue
    $statusCommand = "docker-compose -f $ComposeFile -p $ProjectName ps"
    Invoke-Expression $statusCommand
    
    Write-Host "`n🔗 Service URLs:" -ForegroundColor $colors.Blue
    Write-Host "🌾 FarmMate Web App:     http://localhost:3000" -ForegroundColor $colors.Green
    Write-Host "🚀 Express Backend:      http://localhost:5000" -ForegroundColor $colors.Green
    Write-Host "🐍 Python AI Server:     http://localhost:8000" -ForegroundColor $colors.Green
    Write-Host "🗄️  ChromaDB Service:     http://localhost:8001" -ForegroundColor $colors.Green
    
    Write-Host "`n💾 Docker Resources:" -ForegroundColor $colors.Blue
    Write-Host "Images:"
    docker images | Select-String "farmmate"
    Write-Host "`nVolumes:"
    docker volume ls | Select-String "farmmate"
}

# Function to backup data
function Backup-Data {
    $backupDir = "./backups/$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    
    Write-Host "💾 Creating backup at $backupDir..." -ForegroundColor $colors.Blue
    
    # Backup Docker volumes if they exist
    $volumes = docker volume ls --filter "name=farmmate" --format "{{.Name}}"
    if ($volumes) {
        foreach ($volume in $volumes) {
            Write-Host "📦 Backing up volume: $volume" -ForegroundColor $colors.Yellow
            docker run --rm -v "${volume}:/data" -v "${PWD}/${backupDir}:/backup" alpine tar czf "/backup/${volume}.tar.gz" -C /data .
        }
    } else {
        Write-Host "ℹ️  No FarmMate volumes found to backup" -ForegroundColor $colors.Yellow
    }
    
    Write-Host "✅ Backup completed at $backupDir" -ForegroundColor $colors.Green
}

# Function to restore data
function Restore-Data {
    param([string]$BackupDir)
    
    if (-not (Test-Path $BackupDir)) {
        Write-Host "❌ Backup directory $BackupDir not found" -ForegroundColor $colors.Red
        exit 1
    }
    
    Write-Host "🔄 Restoring from $BackupDir..." -ForegroundColor $colors.Blue
    
    # Stop services
    Stop-Services
    
    # Restore volumes
    $backupFiles = Get-ChildItem -Path $BackupDir -Filter "*.tar.gz"
    foreach ($backupFile in $backupFiles) {
        $volumeName = $backupFile.BaseName -replace "\.tar$", ""
        Write-Host "📦 Restoring volume: $volumeName" -ForegroundColor $colors.Yellow
        docker run --rm -v "${volumeName}:/data" -v "${PWD}/${BackupDir}:/backup" alpine tar xzf "/backup/$($backupFile.Name)" -C /data
    }
    
    Write-Host "✅ Restore completed" -ForegroundColor $colors.Green
}

# Function to update services
function Update-Services {
    Write-Host "🔄 Updating FarmMate services..." -ForegroundColor $colors.Blue
    
    # Pull latest images
    $pullCommand = "docker-compose -f $ComposeFile -p $ProjectName pull"
    Invoke-Expression $pullCommand
    
    # Rebuild and restart
    $updateCommand = "docker-compose -f $ComposeFile -p $ProjectName up -d --build"
    Invoke-Expression $updateCommand
    
    Write-Host "✅ Services updated" -ForegroundColor $colors.Green
}

# Function to open shell
function Open-Shell {
    param([string]$ServiceName = "agent-python")
    
    $shellCommand = "docker-compose -f $ComposeFile -p $ProjectName exec $ServiceName /bin/bash"
    Invoke-Expression $shellCommand
}

# Main script logic
switch ($Command) {
    "start" {
        Test-Docker
        if (-not $SkipPortCheck) {
            if (-not (Test-Ports)) { exit 1 }
        }
        Start-Services
        Show-Status
        
        Write-Host "
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🎉 FARMMATE DEPLOYMENT COMPLETE! 🎉                  ║
║                          All Services Running in Docker                      ║
║                                                                              ║
║  🌾 Web App:    http://localhost:3000                                       ║
║  🚀 Backend:    http://localhost:5000                                       ║
║  🐍 AI Server:  http://localhost:8000                                       ║
║                                                                              ║
║  Use './docker-farmmate.ps1 logs' to view logs                              ║
║  Use './docker-farmmate.ps1 stop' to stop all services                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor $colors.Green
        
        # Open applications in browser
        Start-Process "http://localhost:3000"
    }
    
    "dev" {
        Test-Docker
        if (-not (Test-Ports)) { exit 1 }
        Start-Services -Mode "dev"
        Show-Status
    }
    
    "stop" {
        Stop-Services
    }
    
    "restart" {
        Stop-Services
        Start-Sleep -Seconds 2
        Test-Docker
        Start-Services
    }
    
    "status" {
        Show-Status
    }
    
    "logs" {
        Show-Logs -ServiceName $ServiceName
    }
    
    "cleanup" {
        Invoke-Cleanup
    }
    
    "backup" {
        Backup-Data
    }
    
    "restore" {
        Restore-Data -BackupDir $ServiceName
    }
    
    "update" {
        Update-Services
    }
    
    "build" {
        $buildCommand = "docker-compose -f $ComposeFile -p $ProjectName build --parallel"
        Invoke-Expression $buildCommand
    }
    
    "shell" {
        $service = if ($ServiceName) { $ServiceName } else { "agent-python" }
        Open-Shell -ServiceName $service
    }
    
    default {
        Write-Host "🐳 FarmMate Docker Management Script" -ForegroundColor $colors.Blue
        Write-Host ""
        Write-Host "Usage: .\docker-farmmate.ps1 {start|dev|stop|restart|status|logs|cleanup|backup|restore|update|build|shell}" -ForegroundColor $colors.Yellow
        Write-Host ""
        Write-Host "Commands:"
        Write-Host "  start [-SkipPortCheck]     Start all services in production mode"
        Write-Host "  dev                        Start all services in development mode"
        Write-Host "  stop                       Stop all services"
        Write-Host "  restart                    Restart all services"
        Write-Host "  status                     Show service status and URLs"
        Write-Host "  logs [service]             Show logs for all services or specific service"
        Write-Host "  cleanup                    Stop services and clean up Docker resources"
        Write-Host "  backup                     Create backup of data volumes"
        Write-Host "  restore <backup_dir>       Restore from backup directory"
        Write-Host "  update                     Update all services to latest version"
        Write-Host "  build                      Build all Docker images"
        Write-Host "  shell [service]            Open shell in service container (default: agent-python)"
        Write-Host ""
        Write-Host "Examples:"
        Write-Host "  .\docker-farmmate.ps1 start                   # Start all services"
        Write-Host "  .\docker-farmmate.ps1 dev                     # Start in development mode"
        Write-Host "  .\docker-farmmate.ps1 logs backend            # Show backend service logs"
        Write-Host "  .\docker-farmmate.ps1 shell agent-python      # Open shell in Python AI server"
    }
}
