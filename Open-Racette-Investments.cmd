@echo off
setlocal

set "PROJECT_ROOT=%~dp0"
set "PYTHON=%PROJECT_ROOT%..\..\project2-venv\Scripts\python.exe"
set "APP=%PROJECT_ROOT%research\project2\app.py"

if not exist "%PYTHON%" (
    echo.
    echo Racette Investments needs its one-time setup first.
    echo Open PowerShell in the Work Folder and run:
    echo   python -m venv project2-venv
    echo   .\project2-venv\Scripts\python.exe -m pip install -r "MSFT\ticker-research\requirements.txt"
    echo.
    pause
    exit /b 1
)

echo Starting Racette Investments...
start "Racette Investments server" "%PYTHON%" -m streamlit run "%APP%" --server.headless true --browser.gatherUsageStats false
timeout /t 4 /nobreak >nul
start "" "http://localhost:8501"
exit /b 0
