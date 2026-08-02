@echo off
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 1 /nobreak >nul
start "" http://127.0.0.1:8080
start "" pythonw "%~dp0server.py"