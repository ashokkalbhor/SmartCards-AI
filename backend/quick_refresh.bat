@echo off
REM Quick Database Refresh Script for Windows
REM =========================================

echo.
echo SmartCards AI Quick Database Refresh (Windows)
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

REM Run the quick refresh script
echo Running quick database refresh script...
echo.
python quick_refresh.py

if errorlevel 1 (
    echo.
    echo ERROR: Quick refresh failed!
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo SUCCESS: Quick refresh completed!
echo Database now has fresh sample data
echo.
pause 