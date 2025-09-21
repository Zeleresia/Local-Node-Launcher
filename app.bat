@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python cannot be found on PATH.
  echo Instal Python, and retry.
  pause
  exit /b 1
)

REM
python -c "import importlib; import sys; sys.exit(0) if importlib.util.find_spec('flask') else 1"
if errorlevel 1 (
  echo Installing Flask...
  python -m pip install --upgrade pip >nul
  python -m pip install flask >nul
)

start "" http://127.0.0.1:5000
python app_server.py