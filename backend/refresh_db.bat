@echo off
REM Database Refresh Script for Windows
REM ===================================

echo.
echo SmartCards AI Database Refresh Tool (Windows)
echo ==============================================
echo.

REM Check if we're in the backend directory
if not exist "app" (
    echo ERROR: Please run this script from the backend directory
    echo Current directory: %cd%
    echo Expected to find 'app' folder here
    pause
    exit /b 1
)

REM Check if Python is available
python --version > nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Run the refresh script
echo Running database refresh script...
echo.
python refresh_db.py

if errorlevel 1 (
    echo.
    echo ERROR: Database refresh failed!
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo SUCCESS: Database refresh completed!
echo You can now start the backend server with: python main.py
echo.
pause 