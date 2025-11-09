$repo = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "Stopping web app (backend + frontend) from repository: $repo"

$backendPidFile = Join-Path $repo "backend.pid"
if (Test-Path $backendPidFile) {
    try {
        $processId = [int](Get-Content -Path $backendPidFile -ErrorAction Stop)
        Stop-Process -Id $processId -Force -ErrorAction Stop
        Remove-Item $backendPidFile -Force
        Write-Host "Stopped backend (PID $processId)"
    } catch {
        Write-Host "Failed to stop backend PID from $backendPidFile : $_"
    }
} else {
    Write-Host "No backend.pid file found; backend may not be running or was started manually."
}

$frontendPidFile = Join-Path $repo "frontend.pid"
if (Test-Path $frontendPidFile) {
    try {
        $processId = [int](Get-Content -Path $frontendPidFile -ErrorAction Stop)
        Stop-Process -Id $processId -Force -ErrorAction Stop
        Remove-Item $frontendPidFile -Force
        Write-Host "Stopped frontend (PID $processId)"
    } catch {
        Write-Host "Failed to stop frontend PID from $frontendPidFile : $_"
    }
} else {
    Write-Host "No frontend.pid file found; frontend may not be running or was started manually."
}

Write-Host "Stop script finished. If processes still exist, check Task Manager or run 'Get-Process python,node' in PowerShell." 
