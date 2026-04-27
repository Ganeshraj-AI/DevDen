@echo off
echo ==============================================
echo      Deploying devden-v4 to Production
echo ==============================================
echo.

echo [1/4] Checking python environment...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH!
    exit /b 1
)

echo [2/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies!
    exit /b 1
)

echo [3/4] Starting Waitress production server...
echo Server will run at http://localhost:5000/
echo Press Ctrl+C to stop the server.
echo.

REM Read PORT from .env if possible, otherwise default to 5000
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.environ.get('PORT', '5000'))" > temp_port.txt
set /p PORT=<temp_port.txt
del temp_port.txt

python -m waitress --port=%PORT% app:app
