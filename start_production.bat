@echo off
title Tamimah Prospecting Intelligence - Production Runner
echo ===================================================
echo Starting Tamimah Prospecting Intelligence System
echo ===================================================

cd /d "%~dp0"

:: Set path to portable node and python
set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%LOCALAPPDATA%\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"

echo [1/3] Starting WhatsApp Gateway on port 3001...
start "WhatsApp Gateway" /min cmd /c "cd gateway && node server.js"

timeout /t 3 /nobreak >nul

echo [2/3] Starting Intelligence Dashboard & Scheduler on port 8000...
start "Tamimah Dashboard" /min cmd /c "python app.py"

timeout /t 2 /nobreak >nul

echo [3/3] Starting Cloudflare Public Tunnel...
start "Cloudflare Tunnel" /min cmd /c "cloudflared.exe tunnel --url http://localhost:8000"

echo ===================================================
echo System is LIVE!
echo Local Dashboard: http://localhost:8000
echo WhatsApp Gateway: http://localhost:3001/qr
echo ===================================================
timeout /t 5
