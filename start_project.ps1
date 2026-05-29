# Melanoma AI Detection System Startup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Melanoma AI Detection System Startup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "C:\Melanoma AI Detection System"

# Check virtual environment
Write-Host "Checking virtual environment..." -ForegroundColor Yellow
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it first using: python -m venv .venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Flask Application..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Application will be available at: http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the application
python app.py

# Keep window open if there's an error
Read-Host "Press Enter to exit"