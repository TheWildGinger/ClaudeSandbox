@echo off
REM EngiCalc Development Server Launcher (Windows)

echo ========================================
echo   EngiCalc Development Server
echo ========================================
echo.

REM Check if Poetry is installed
where poetry >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Poetry is not installed
    echo Install it from: https://python-poetry.org/docs/#installation
    exit /b 1
)

REM Check if Node is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed
    echo Install it from: https://nodejs.org/
    exit /b 1
)

REM Install backend dependencies if needed
if not exist "backend\.venv" (
    echo Installing backend dependencies...
    cd backend
    poetry install
    cd ..
)

REM Install frontend dependencies if needed
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    npm install
    cd ..
)

echo.
echo Starting servers...
echo.

REM Start backend in new window
start "EngiCalc Backend" cmd /k "cd backend && poetry run python -m app.main"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in new window
start "EngiCalc Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   EngiCalc is running!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop the servers
echo.
