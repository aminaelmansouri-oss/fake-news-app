# Start Fake News Detection API Server
# Run from PowerShell: .\start_server.ps1

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$agentDir = Join-Path $projectRoot "fake_news_agent"
$pythonExe = Join-Path $projectRoot ".venv\Scripts\python.exe"

Write-Host "Starting Fake News Detection Server..." -ForegroundColor Green
Write-Host "Directory: $agentDir" -ForegroundColor Cyan
Write-Host ""

# Change to the agent directory
Set-Location $agentDir

# Launch uvicorn
& $pythonExe -m uvicorn api:app --host 0.0.0.0 --port 8000 --reload

Write-Host ""
Write-Host "Server closed" -ForegroundColor Yellow
