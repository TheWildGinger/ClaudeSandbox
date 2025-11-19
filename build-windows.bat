@echo off
REM Build script for creating EngiCalc.exe on Windows

echo ================================================
echo Building EngiCalc Standalone Executable
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [Step 1/5] Installing Poetry if needed...
pip install poetry
if errorlevel 1 (
    echo ERROR: Failed to install Poetry
    pause
    exit /b 1
)
echo.

echo [Step 2/5] Building frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install frontend dependencies
    pause
    exit /b 1
)
call npm run build
if errorlevel 1 (
    echo ERROR: Failed to build frontend
    pause
    exit /b 1
)
cd ..
echo.

echo [Step 3/5] Installing backend dependencies...
cd backend
call poetry install
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo.

echo [Step 4/5] Installing PyInstaller...
call poetry add pyinstaller --group dev
echo.

echo [Step 5/5] Building executable...
call poetry run pyinstaller ..\EngiCalc.spec --clean
if errorlevel 1 (
    echo ERROR: Failed to build executable
    pause
    exit /b 1
)
echo.

echo ================================================
echo Build Complete!
echo ================================================
echo.
echo Your executable is located at:
echo backend\dist\EngiCalc.exe
echo.
echo File size:
dir dist\EngiCalc.exe | find "EngiCalc.exe"
echo.
echo You can now copy EngiCalc.exe to your Windows desktop
echo and run it by double-clicking!
echo.
pause
