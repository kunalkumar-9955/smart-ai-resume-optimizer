$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot
$python = Join-Path $projectRoot 'venv\Scripts\python.exe'
if (Test-Path $python) {
    & $python app.py
} else {
    Write-Host 'Virtual environment not found. Run: python -m venv venv' -ForegroundColor Yellow
}
