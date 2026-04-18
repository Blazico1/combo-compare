$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host "Starting web app (backend + frontend) from repository: $repo"

# Function to check if a process is running by PID
function Test-ProcessRunning {
    param([int]$Pid)
    try {
        $proc = Get-Process -Id $Pid -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Function to find running processes related to this repo
function Find-RepoProcesses {
    param([string]$RepoPath)
    $processes = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine.Contains($RepoPath) } | Select-Object ProcessId, Name, CommandLine
    return $processes
}

# Check if already running
$backendPidFile = Join-Path $repo "backend.pid"
$frontendPidFile = Join-Path $repo "frontend.pid"

$alreadyRunning = $false
if ((Test-Path $backendPidFile) -or (Test-Path $frontendPidFile)) {
    Write-Host "PID files exist. Checking if processes are still running..."
    if (Test-Path $backendPidFile) {
        $pid = [int](Get-Content $backendPidFile -ErrorAction SilentlyContinue)
        if (Test-ProcessRunning $pid) {
            Write-Host "Backend appears to be running (PID $pid). Please stop it first."
            $alreadyRunning = $true
        } else {
            Remove-Item $backendPidFile -ErrorAction SilentlyContinue
        }
    }
    if (Test-Path $frontendPidFile) {
        $pid = [int](Get-Content $frontendPidFile -ErrorAction SilentlyContinue)
        if (Test-ProcessRunning $pid) {
            Write-Host "Frontend appears to be running (PID $pid). Please stop it first."
            $alreadyRunning = $true
        } else {
            Remove-Item $frontendPidFile -ErrorAction SilentlyContinue
        }
    }
}

# Also check for any repo-related processes
$repoProcesses = Find-RepoProcesses $repo
if ($repoProcesses) {
    Write-Host "Found existing processes related to this repo:"
    $repoProcesses | ForEach-Object { Write-Host "  $($_.Name) (PID $($_.ProcessId)): $($_.CommandLine)" }
    Write-Host "Please stop them manually or use the stop script."
    $alreadyRunning = $true
}

if ($alreadyRunning) {
    Write-Host "Aborting start due to existing processes."
    exit 1
}

# Paths
$backendVenv = Join-Path $repo "backend\venv"
$backendPython = Join-Path $backendVenv "Scripts\python.exe"
$backendPip = Join-Path $backendVenv "Scripts\pip.exe"
$backendMain = Join-Path $repo "backend\main.py"
$backendOut = Join-Path $repo "backend\backend.log"
$backendErr = Join-Path $repo "backend\backend.err.log"

$frontendDir = Join-Path $repo "frontend"
$frontendOut = Join-Path $frontendDir "frontend.log"
$frontendErr = Join-Path $frontendDir "frontend.err.log"

Write-Host "Preparing backend..."

# Ensure Python is available
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "Python is not available in PATH. Please install Python 3.10+ and try again."; exit 1
}

# Create backend venv if missing
if (-not (Test-Path $backendPython)) {
    Write-Host "Backend virtualenv not found. Creating at: $backendVenv"
    & $pythonCmd.Path -m venv $backendVenv
    if (-not (Test-Path $backendPython)) {
        Write-Host "Failed to create backend venv at $backendVenv"; exit 1
    }
}

# Install Python requirements (prefer backend/requirements.txt else root requirements.txt)
$reqFileBackend = Join-Path $repo "backend\requirements.txt"
$reqFileRoot = Join-Path $repo "requirements.txt"
$reqToUse = if (Test-Path $reqFileBackend) { $reqFileBackend } elseif (Test-Path $reqFileRoot) { $reqFileRoot } else { $null }
if ($reqToUse) {
    Write-Host "Installing Python requirements from $reqToUse"
    & $backendPip install -r $reqToUse
} else {
    Write-Host "No requirements.txt found; skipping pip install"
}

Write-Host "Starting backend using venv Python: $backendPython"
try {
    # Run uvicorn inside the backend venv via python -m uvicorn so the environment is used.
    # Use module `main:app` since the working directory is the backend folder.
    $uvicornArgs = "-m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
    $be = Start-Process -FilePath $backendPython -ArgumentList $uvicornArgs -WorkingDirectory (Join-Path $repo "backend") -RedirectStandardOutput $backendOut -RedirectStandardError $backendErr -WindowStyle Hidden -PassThru
    if ($be) {
        $be.Id | Out-File -FilePath $backendPidFile -Encoding ascii
        Write-Host "Backend started (PID $($be.Id)). Logs: $backendOut, $backendErr"
    } else {
        Write-Host "Failed to start backend process. Check $backendOut and $backendErr for details."
    }
} catch {
    Write-Host "Error starting backend: $_"; exit 1
}

Write-Host "Preparing frontend..."

if (-not (Test-Path $frontendDir)) {
    Write-Host "No frontend folder found at: $frontendDir"; exit 1
}

# Ensure Node/npm is available
$npmCmd = Get-Command npm -ErrorAction SilentlyContinue
if (-not $npmCmd) {
    Write-Host "npm not found in PATH. Please install Node.js and npm (https://nodejs.org/) and re-run this script."; exit 1
}

# Install node modules if node_modules missing
if (-not (Test-Path (Join-Path $frontendDir "node_modules"))) {
    Write-Host "Installing frontend packages (npm install)..."
    # Run npm install synchronously so dependencies are available
    $installArgs = "-NoProfile -ExecutionPolicy Bypass -Command cd `"$frontendDir`"; npm install"
    $installProc = Start-Process -FilePath (Get-Command powershell).Path -ArgumentList $installArgs -Wait -NoNewWindow -PassThru
    if ($installProc.ExitCode -ne 0) { Write-Host "npm install failed (exit $($installProc.ExitCode)). Check logs."; exit 1 }
}

Write-Host "Starting frontend (npm run dev) in: $frontendDir"
# Run npm through a new PowerShell process to avoid executing the npm.ps1 shim directly
$pwshPath = (Get-Command powershell).Path
$args = @('-NoProfile','-ExecutionPolicy','Bypass','-Command', "cd `"$frontendDir`"; npm run dev -- --host 0.0.0.0 --port 3000")
try {
    $fe = Start-Process -FilePath $pwshPath -ArgumentList $args -WorkingDirectory $frontendDir -RedirectStandardOutput $frontendOut -RedirectStandardError $frontendErr -WindowStyle Hidden -PassThru
    if ($fe) {
        $fe.Id | Out-File -FilePath $frontendPidFile -Encoding ascii
        Write-Host "Frontend started (PID $($fe.Id)). Logs: $frontendOut, $frontendErr"
    } else {
        Write-Host "Failed to start frontend process. Check $frontendOut and $frontendErr for details."; exit 1
    }
} catch {
    Write-Host "Error starting frontend: $_"; exit 1
}

Write-Host "Start script finished. Backend PID file: $backendPidFile; Frontend PID file: $frontendPidFile"
