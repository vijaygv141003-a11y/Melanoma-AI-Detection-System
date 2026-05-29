@echo off
echo ========================================
echo Melanoma AI Detection System Startup
echo ========================================
echo.

cd /d "C:\Melanoma AI Detection System"

echo Checking virtual environment...
if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment not found!
    echo Please create it first using: python -m venv .venv
    pause
    exit /b 1
)

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Checking dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo Starting Flask Application...
echo ========================================
echo.
echo Application will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause