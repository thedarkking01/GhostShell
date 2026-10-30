@echo off
echo.
echo  ^>^>^> GhostShell starting...
echo.

REM Check Ollama is installed
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo  [ERROR] Ollama not found. Download it from https://ollama.com
    pause
    exit /b 1
)

REM Start Ollama serve in background if not already running
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo  Starting Ollama...
    start /min cmd /c "ollama serve"
    timeout /t 3 /nobreak >nul
) else (
    echo  Ollama already running.
)

REM Start the FastAPI server
echo  Starting GhostShell server at http://localhost:8000
echo  Press Ctrl+C to stop.
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
