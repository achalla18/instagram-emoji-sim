@echo off
title Emoji Reactions - Web Version
echo.
echo  ========================================
echo   Emoji Reactions -- Web Version
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

:: Navigate to web directory
cd /d "%~dp0\..\src\web"

echo  Starting web server on http://localhost:8080
echo  Press Ctrl+C to stop.
echo.

:: Open browser after a short delay
start "" "http://localhost:8080"

:: Start Python HTTP server
python -m http.server 8080

pause
