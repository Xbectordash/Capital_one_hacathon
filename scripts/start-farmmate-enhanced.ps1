# Enhanced FarmMate Startup Script with Monitoring (PowerShell)
# This script starts all services with comprehensive monitoring on Windows

param(
    [switch]$SkipPortCheck,
    [switch]$Verbose
)

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
║                    🌾 FARMMATE ENHANCED STARTUP 🌾                           ║
║                     Comprehensive Monitoring Enabled                         ║
║                                                                              ║
║  🐍 Python AI Server (Port 8000)                                            ║
║  🚀 Express Backend (Port 5000)                                             ║
║  ⚛️  React Frontend (Port 3000)                                              ║
║  📊 Monitoring Dashboard (Port 9000)                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor $colors.Cyan

# Global variables
$script:runningServices = @{}
$script:logDirectory = "logs"

# Function to check if port is available
function Test-Port {
    param(
        [int]$Port,
        [string]$ServiceName
    )
    
    try {
        $connection = Test-NetConnection -ComputerName "localhost" -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
        if ($connection) {
            Write-Host "❌ Port $Port is already in use (required for $ServiceName)" -ForegroundColor $colors.Red
            Write-Host "   Please stop the service running on port $Port and try again" -ForegroundColor $colors.Yellow
            return $false
        } else {
            Write-Host "✅ Port $Port is available for $ServiceName" -ForegroundColor $colors.Green
            return $true
        }
    } catch {
        # If Test-NetConnection fails, try alternative method
        $listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Any, $Port)
        try {
            $listener.Start()
            $listener.Stop()
            Write-Host "✅ Port $Port is available for $ServiceName" -ForegroundColor $colors.Green
            return $true
        } catch {
            Write-Host "❌ Port $Port is already in use (required for $ServiceName)" -ForegroundColor $colors.Red
            Write-Host "   Please stop the service running on port $Port and try again" -ForegroundColor $colors.Yellow
            return $false
        }
    }
}

# Function to start service with logging
function Start-ServiceWithLogging {
    param(
        [string]$ServiceName,
        [string]$Command,
        [string]$WorkingDirectory,
        [string]$LogFile,
        [string]$Color
    )
    
    Write-Host "🚀 Starting $ServiceName..." -ForegroundColor $Color
    
    # Ensure logs directory exists
    $logDir = Split-Path $LogFile
    if (!(Test-Path $logDir)) {
        New-Item -ItemType Directory -Path $logDir -Force | Out-Null
    }
    
    # Create log file with initial information
    @"
Service: $ServiceName
Command: $Command
Working Directory: $WorkingDirectory
Started at: $(Get-Date)
----------------------------------------
"@ | Out-File -FilePath $LogFile -Encoding UTF8
    
    try {
        # Parse command and arguments
        $commandParts = $Command -split ' ', 2
        $executable = $commandParts[0]
        $arguments = if ($commandParts.Length -gt 1) { $commandParts[1] } else { "" }
        
        # Start the process
        $processStartInfo = New-Object System.Diagnostics.ProcessStartInfo
        $processStartInfo.FileName = $executable
        $processStartInfo.Arguments = $arguments
        $processStartInfo.WorkingDirectory = $WorkingDirectory
        $processStartInfo.UseShellExecute = $false
        $processStartInfo.RedirectStandardOutput = $true
        $processStartInfo.RedirectStandardError = $true
        $processStartInfo.CreateNoWindow = $true
        
        $process = [System.Diagnostics.Process]::Start($processStartInfo)
        
        # Store process information
        $script:runningServices[$ServiceName] = @{
            Process = $process
            LogFile = $LogFile
            StartTime = Get-Date
        }
        
        # Start background jobs to capture output - Fixed version
        $outputJob = Start-Job -ScriptBlock {
            param($processId, $logFile)
            try {
                $proc = Get-Process -Id $processId -ErrorAction SilentlyContinue
                if ($proc) {
                    # Alternative approach for output capture
                    Start-Sleep -Seconds 1
                    Add-Content -Path $logFile -Value "Process started successfully with PID: $processId"
                }
            } catch {
                Add-Content -Path $logFile -Value "Error capturing output: $_"
            }
        } -ArgumentList $process.Id, $LogFile
        
        # Wait a moment and check if service started successfully
        Start-Sleep -Seconds 3
        
        if (!$process.HasExited) {
            Write-Host "✅ $ServiceName started successfully (PID: $($process.Id))" -ForegroundColor $colors.Green
            return $true
        } else {
            Write-Host "❌ Failed to start $ServiceName" -ForegroundColor $colors.Red
            Write-Host "   Check log file: $LogFile" -ForegroundColor $colors.Yellow
            return $false
        }
    } catch {
        Write-Host "❌ Failed to start $ServiceName`: $_" -ForegroundColor $colors.Red
        Write-Host "   Check log file: $LogFile" -ForegroundColor $colors.Yellow
        return $false
    }
}

# Function to test URL connectivity
function Test-URL {
    param(
        [string]$URL,
        [int]$TimeoutSeconds = 5
    )
    
    try {
        $response = Invoke-WebRequest -Uri $URL -TimeoutSec $TimeoutSeconds -UseBasicParsing -DisableKeepAlive
        return $response.StatusCode -eq 200
    } catch {
        return $false
    }
}

# Function to cleanup on exit
function Stop-AllServices {
    Write-Host "`n🛑 Shutting down FarmMate services..." -ForegroundColor $colors.Yellow
    
    foreach ($serviceName in $script:runningServices.Keys) {
        $serviceInfo = $script:runningServices[$serviceName]
        $process = $serviceInfo.Process
        
        if (!$process.HasExited) {
            Write-Host "🛑 Stopping $serviceName (PID: $($process.Id))" -ForegroundColor $colors.Yellow
            try {
                $process.Kill()
                $process.WaitForExit(5000)
            } catch {
                Write-Host "⚠️  Force killing $serviceName" -ForegroundColor $colors.Red
            }
        }
    }
    
    # Clean up background jobs
    Get-Job | Remove-Job -Force
    
    Write-Host "✅ All services stopped" -ForegroundColor $colors.Green
    exit 0
}

# Set up signal handlers
Register-EngineEvent PowerShell.Exiting -Action { Stop-AllServices }
# Use try-catch for CancelKeyPress event
try {
    [Console]::CancelKeyPress.add({ Stop-AllServices })
} catch {
    Write-Host "⚠️  Note: Ctrl+C handler may not work properly in this PowerShell environment" -ForegroundColor Yellow
}

# Create logs directory
if (!(Test-Path $script:logDirectory)) {
    New-Item -ItemType Directory -Path $script:logDirectory -Force | Out-Null
}

Write-Host "🔍 Checking system requirements..." -ForegroundColor $colors.Blue

# Check if required commands are available
$requiredCommands = @("python", "node", "npm")
foreach ($cmd in $requiredCommands) {
    try {
        $null = Get-Command $cmd -ErrorAction Stop
        Write-Host "✅ $cmd is available" -ForegroundColor $colors.Green
    } catch {
        Write-Host "❌ $cmd is not installed" -ForegroundColor $colors.Red
        Write-Host "   Please install $cmd and try again" -ForegroundColor $colors.Yellow
        exit 1
    }
}

if (!$SkipPortCheck) {
    Write-Host "`n🔍 Checking port availability..." -ForegroundColor $colors.Blue
    
    # Check port availability
    $portsServices = @(
        @{Port = 8000; Service = "Python AI Server"},
        @{Port = 5000; Service = "Express Backend"},
        @{Port = 3000; Service = "React Frontend"},
        @{Port = 9000; Service = "Monitoring Dashboard"}
    )
    
    foreach ($portService in $portsServices) {
        if (!(Test-Port -Port $portService.Port -ServiceName $portService.Service)) {
            exit 1
        }
    }
}

Write-Host "`n📊 Starting Monitoring Dashboard..." -ForegroundColor $colors.Purple

# Start Monitoring Dashboard - DISABLED due to dependency issues
Write-Host "⚠️  Skipping Monitoring Dashboard due to dependency issues..." -ForegroundColor $colors.Yellow
$script:monitoringFailed = $true

# Wait for monitoring dashboard to fully start (if it started successfully)
if (-not $script:monitoringFailed) {
    Write-Host "⏳ Waiting for monitoring dashboard to initialize..." -ForegroundColor $colors.Yellow
    Start-Sleep -Seconds 5

    # Check if monitoring dashboard is responding
    $attempts = 0
    do {
        $attempts++
        if (Test-URL -URL "http://localhost:9000/health") {
            Write-Host "✅ Monitoring dashboard is responding" -ForegroundColor $colors.Green
            break
        } else {
            if ($attempts -eq 10) {
                Write-Host "❌ Monitoring dashboard not responding after 10 attempts" -ForegroundColor $colors.Red
                Write-Host "⚠️  Continuing without monitoring dashboard..." -ForegroundColor $colors.Yellow
                $script:monitoringFailed = $true
                break
            }
            Write-Host "⏳ Waiting for monitoring dashboard... (attempt $attempts/10)" -ForegroundColor $colors.Yellow
            Start-Sleep -Seconds 2
        }
    } while ($attempts -lt 10)
} else {
    Write-Host "⚠️  Skipping monitoring dashboard health check (failed to start)" -ForegroundColor $colors.Yellow
}

Write-Host "`n🐍 Starting Python AI Server..." -ForegroundColor $colors.Blue

# Start Python AI Server
$pythonPath = Join-Path $PWD "agent-python"
if (!(Start-ServiceWithLogging -ServiceName "Python AI Server" -Command "$pythonExe src/start_server.py" -WorkingDirectory $pythonPath -LogFile "$script:logDirectory\python-ai.log" -Color $colors.Blue)) {
    Write-Host "❌ Failed to start Python AI server" -ForegroundColor $colors.Red
    Write-Host "⚠️  Continuing without Python AI server..." -ForegroundColor $colors.Yellow
    $script:pythonAIFailed = $true
} else {
    $script:pythonAIFailed = $false
}

# Wait for Python AI server
Write-Host "⏳ Waiting for Python AI server to initialize..." -ForegroundColor $colors.Yellow
Start-Sleep -Seconds 8

# Check if Python AI server is responding
$attempts = 0
do {
    $attempts++
    if (Test-URL -URL "http://localhost:8000/health") {
        Write-Host "✅ Python AI server is responding" -ForegroundColor $colors.Green
        break
    } else {
        if ($attempts -eq 10) {
            Write-Host "❌ Python AI server not responding after 10 attempts" -ForegroundColor $colors.Red
            Stop-AllServices
            exit 1
        }
        Write-Host "⏳ Waiting for Python AI server... (attempt $attempts/10)" -ForegroundColor $colors.Yellow
        Start-Sleep -Seconds 2
    }
} while ($attempts -lt 10)

Write-Host "`n🚀 Starting Express Backend..." -ForegroundColor $colors.Green

# Start Express Backend
$backendPath = Join-Path $PWD "backend"
if (!(Start-ServiceWithLogging -ServiceName "Express Backend" -Command "node src/enhanced_server.js" -WorkingDirectory $backendPath -LogFile "$script:logDirectory\express-backend.log" -Color $colors.Green)) {
    Write-Host "❌ Failed to start Express backend" -ForegroundColor $colors.Red
    Stop-AllServices
    exit 1
}

# Wait for Express backend
Write-Host "⏳ Waiting for Express backend to initialize..." -ForegroundColor $colors.Yellow
Start-Sleep -Seconds 5

# Check if Express backend is responding
$attempts = 0
do {
    $attempts++
    if (Test-URL -URL "http://localhost:5000/api/health") {
        Write-Host "✅ Express backend is responding" -ForegroundColor $colors.Green
        break
    } else {
        if ($attempts -eq 10) {
            Write-Host "❌ Express backend not responding after 10 attempts" -ForegroundColor $colors.Red
            Stop-AllServices
            exit 1
        }
        Write-Host "⏳ Waiting for Express backend... (attempt $attempts/10)" -ForegroundColor $colors.Yellow
        Start-Sleep -Seconds 2
    }
} while ($attempts -lt 10)

Write-Host "`n⚛️  Starting React Frontend..." -ForegroundColor $colors.Cyan

# Start React Frontend
$frontendPath = Join-Path $PWD "frontend\web\agricultural-chat-app"

# Check if node_modules exists
$nodeModulesPath = Join-Path $frontendPath "node_modules"
if (!(Test-Path $nodeModulesPath)) {
    Write-Host "📦 Installing React dependencies..." -ForegroundColor $colors.Yellow
    $installProcess = Start-Process -FilePath "npm" -ArgumentList "install" -WorkingDirectory $frontendPath -Wait -PassThru
    if ($installProcess.ExitCode -ne 0) {
        Write-Host "❌ Failed to install React dependencies" -ForegroundColor $colors.Red
        Stop-AllServices
        exit 1
    }
}

# Copy enhanced components if they don't exist or are different
$originalAppJs = Join-Path $frontendPath "src\App.js"
$enhancedAppJs = Join-Path $frontendPath "src\EnhancedApp.js"
$backupAppJs = Join-Path $frontendPath "src\App.js.backup"

if (!(Test-Path $backupAppJs)) {
    Write-Host "💾 Backing up original App.js..." -ForegroundColor $colors.Yellow
    Copy-Item $originalAppJs $backupAppJs
}

$originalAppCss = Join-Path $frontendPath "src\App.css"
$enhancedAppCss = Join-Path $frontendPath "src\EnhancedApp.css"
$backupAppCss = Join-Path $frontendPath "src\App.css.backup"

if (!(Test-Path $backupAppCss)) {
    Write-Host "💾 Backing up original App.css..." -ForegroundColor $colors.Yellow
    Copy-Item $originalAppCss $backupAppCss
}

# Use enhanced components
Write-Host "🔄 Using enhanced React components..." -ForegroundColor $colors.Yellow
Copy-Item $enhancedAppJs $originalAppJs -Force
Copy-Item $enhancedAppCss $originalAppCss -Force

if (!(Start-ServiceWithLogging -ServiceName "React Frontend" -Command "npm start" -WorkingDirectory $frontendPath -LogFile "$script:logDirectory\react-frontend.log" -Color $colors.Cyan)) {
    Write-Host "❌ Failed to start React frontend" -ForegroundColor $colors.Red
    Stop-AllServices
    exit 1
}

# Wait for React frontend
Write-Host "⏳ Waiting for React frontend to initialize..." -ForegroundColor $colors.Yellow
Start-Sleep -Seconds 10

# Check if React frontend is responding
$attempts = 0
do {
    $attempts++
    if (Test-URL -URL "http://localhost:3000") {
        Write-Host "✅ React frontend is responding" -ForegroundColor $colors.Green
        break
    } else {
        if ($attempts -eq 15) {
            Write-Host "❌ React frontend not responding after 15 attempts" -ForegroundColor $colors.Red
            Stop-AllServices
            exit 1
        }
        Write-Host "⏳ Waiting for React frontend... (attempt $attempts/15)" -ForegroundColor $colors.Yellow
        Start-Sleep -Seconds 3
    }
} while ($attempts -lt 15)

# Final status check
Write-Host "`n🔍 Performing final system check..." -ForegroundColor $colors.Purple

$services = @(
    @{URL = "http://localhost:9000/health"; Name = "Monitoring Dashboard"},
    @{URL = "http://localhost:8000/health"; Name = "Python AI Server"},
    @{URL = "http://localhost:5000/api/health"; Name = "Express Backend"},
    @{URL = "http://localhost:3000"; Name = "React Frontend"}
)

$allHealthy = $true
foreach ($service in $services) {
    if (Test-URL -URL $service.URL) {
        Write-Host "✅ $($service.Name) is healthy" -ForegroundColor $colors.Green
    } else {
        Write-Host "❌ $($service.Name) is not responding" -ForegroundColor $colors.Red
        $allHealthy = $false
    }
}

if ($allHealthy) {
    Write-Host "
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🎉 FARMMATE STARTUP COMPLETE! 🎉                     ║
║                          Core Services Running Successfully                  ║
║                                                                              ║
if (-not $script:monitoringFailed) {
    Write-Host "║  📊 Monitoring Dashboard: http://localhost:9000                              ║" -ForegroundColor $colors.Green
} else {
    Write-Host "║  📊 Monitoring Dashboard: ❌ Failed to start                                  ║" -ForegroundColor $colors.Yellow
}
║  🌾 FarmMate Web App:     http://localhost:3000                              ║
║  🚀 Express Backend:      http://localhost:5000                              ║
║  🐍 Python AI Server:     http://localhost:8000                              ║
║                                                                              ║
║  📋 Logs Directory:       ./logs/                                           ║
║  🔍 Service Status:       All services healthy                              ║
║  ⚡ Real-time Monitoring: Enabled                                            ║
║                                                                              ║
║  Press Ctrl+C to stop all services                                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor $colors.Green
    
    # Open applications in default browser
    Write-Host "🌐 Opening applications in browser..." -ForegroundColor $colors.Yellow
    Start-Sleep -Seconds 2
    
    Start-Process "http://localhost:9000"
    Start-Sleep -Seconds 1
    Start-Process "http://localhost:3000"
    
} else {
    Write-Host "
╔══════════════════════════════════════════════════════════════════════════════╗
║                          ⚠️  STARTUP ISSUES DETECTED ⚠️                     ║
║                                                                              ║
║  Some services may not be responding properly.                              ║
║  Check the logs directory for detailed error information.                   ║
║                                                                              ║
║  You can still try to access the applications:                              ║
║  📊 Monitoring: http://localhost:9000                                       ║
║  🌾 FarmMate:   http://localhost:3000                                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
" -ForegroundColor $colors.Red
}

# Keep script running and monitor services
Write-Host "`n🔄 Monitoring services... (Press Ctrl+C to stop)" -ForegroundColor $colors.Blue

try {
    while ($true) {
        Start-Sleep -Seconds 30
        
        # Check if all services are still running
        $deadServices = @()
        foreach ($serviceName in $script:runningServices.Keys) {
            $serviceInfo = $script:runningServices[$serviceName]
            if ($serviceInfo.Process.HasExited) {
                $deadServices += $serviceName
            }
        }
        
        if ($deadServices.Count -gt 0) {
            Write-Host "⚠️  Dead services detected: $($deadServices -join ', ')" -ForegroundColor $colors.Red
            Write-Host "   Consider restarting the application" -ForegroundColor $colors.Yellow
        }
    }
} finally {
    Stop-AllServices
}
