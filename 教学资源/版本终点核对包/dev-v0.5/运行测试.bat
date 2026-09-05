@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment is missing.
    echo Run the setup script first.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pytest -q
pause

