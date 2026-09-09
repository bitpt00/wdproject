@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Virtual environment is missing. Running setup first...
    py -3.11 -m venv .venv 2>nul
    if errorlevel 1 python -m venv .venv
    if exist ".venv\Scripts\python.exe" ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Teaching platform cannot start because .venv is unavailable.
    echo Check that Python is installed and available on PATH.
    pause
    exit /b 1
)

echo Starting the S0 to dev-v0.1 teaching platform...
echo Browser address: http://127.0.0.1:8000
echo Close this window to stop the platform.
echo.

".venv\Scripts\python.exe" -m teaching_platform.app
if errorlevel 1 (
    echo.
    echo The teaching platform exited with an error.
    echo Keep the message above and ask the teacher for help.
    pause
)
