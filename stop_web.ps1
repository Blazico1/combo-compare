$repo = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "Stopping web app (backend + frontend) from repository: $repo"

# Function to kill a process tree safely
function Stop-ProcessTree {
    param([int]$ProcessId)
    try {
        Start-Process -FilePath 'taskkill' -ArgumentList "/PID $ProcessId /F /T" -NoNewWindow -Wait -ErrorAction Stop
        Write-Host "Stopped process tree for PID $ProcessId"
    } catch {
        Write-Host "Failed to stop PID $ProcessId : $_"
    }
}

# Function to find running processes related to this repo
function Find-RepoProcesses {
    param([string]$RepoPath)
    $processes = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine.Contains($RepoPath) } | Select-Object ProcessId, Name, CommandLine
    return $processes
}

# Stop via PID files
$backendPidFile = Join-Path $repo "backend.pid"
if (Test-Path $backendPidFile) {
    try {
        $processId = [int](Get-Content -Path $backendPidFile -ErrorAction Stop)
        Stop-ProcessTree $processId
        Remove-Item $backendPidFile -Force
        Write-Host "Stopped backend (PID $processId)"
    } catch {
        Write-Host "Failed to stop backend PID from $backendPidFile : $_"
    }
} else {
    Write-Host "No backend.pid file found."
}

$frontendPidFile = Join-Path $repo "frontend.pid"
if (Test-Path $frontendPidFile) {
    try {
        $processId = [int](Get-Content -Path $frontendPidFile -ErrorAction Stop)
        Stop-ProcessTree $processId
        Remove-Item $frontendPidFile -Force
        Write-Host "Stopped frontend (PID $processId)"
    } catch {
        Write-Host "Failed to stop frontend PID from $frontendPidFile : $_"
    }
} else {
    Write-Host "No frontend.pid file found."
}

# If no PID files, search for repo-related processes and stop them
$repoProcesses = Find-RepoProcesses $repo
if ($repoProcesses) {
    Write-Host "Found running processes related to this repo. Stopping them..."
    $repoProcesses | ForEach-Object {
        Write-Host "Stopping $($_.Name) (PID $($_.ProcessId)): $($_.CommandLine)"
        Stop-ProcessTree $_.ProcessId
    }
} else {
    Write-Host "No repo-related processes found."
}

Write-Host "Stop script finished."