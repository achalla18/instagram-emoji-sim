@echo off
title Emoji Reactions - Desktop App
echo.
echo  ========================================
echo   Emoji Reactions -- Desktop App
echo  ========================================
echo.

:: Check for Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

:: Navigate to script directory
cd /d "%~dp0\.."

:: Run the desktop app
echo  Starting desktop app...
echo.
python src\python\app.py

if %errorlevel% neq 0 (
    echo.
    echo  [ERROR] App crashed. Check the error above.
    pause
)
