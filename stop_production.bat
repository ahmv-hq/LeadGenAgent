@echo off
title Stop Tamimah Prospecting Services
echo Stopping all Tamimah Prospecting background processes...
taskkill /f /im node.exe /t 2>nul
taskkill /f /im python.exe /t 2>nul
taskkill /f /im cloudflared.exe /t 2>nul
echo Done! All services stopped.
pause
