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

echo [Step 1/5] Checking for Poetry...
echo Trying to detect Poetry installation...
poetry --version >nul 2>&1
if errorlevel 1 (
    echo Poetry not found in PATH. Trying python -m poetry...
    python -m poetry --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo Poetry is not installed. Installing Poetry...
        echo.
        echo OPTION 1: Install via pip (recommended for Windows)
        pip install poetry
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to install Poetry via pip.
            echo.
            echo Please install Poetry manually using one of these methods:
            echo   1. Run in PowerShell: (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content ^| py -
            echo   2. Or visit: https://python-poetry.org/docs/#installation
            echo.
            echo After installing Poetry, close this window, open a NEW Command Prompt, and run this script again.
            pause
            exit /b 1
        )
        echo.
        echo Poetry installed! You may need to close this window and open a NEW Command Prompt.
        echo Trying to continue anyway...
        echo.
    ) else (
        echo Found: python -m poetry
        set POETRY_CMD=python -m poetry
        goto :poetry_found
    )
) else (
    echo Found: poetry
    set POETRY_CMD=poetry
    goto :poetry_found
)

REM Try one more time after installation
poetry --version >nul 2>&1
if errorlevel 1 (
    python -m poetry --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERROR: Poetry was installed but still cannot be found.
        echo Please close this window, open a NEW Command Prompt, and run this script again.
        pause
        exit /b 1
    ) else (
        set POETRY_CMD=python -m poetry
    )
) else (
    set POETRY_CMD=poetry
)

:poetry_found
echo Using: %POETRY_CMD%
echo.

echo [Step 2/5] Building frontend...
cd frontend
if not exist "node_modules\" (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo ERROR: Failed to install frontend dependencies
        echo Make sure Node.js and npm are installed from https://nodejs.org/
        cd ..
        pause
        exit /b 1
    )
)
echo Building frontend...
call npm run build
if errorlevel 1 (
    echo ERROR: Failed to build frontend
    cd ..
    pause
    exit /b 1
)
cd ..
echo Frontend build complete!
echo.

echo [Step 3/5] Installing backend dependencies...
cd backend
call %POETRY_CMD% install
if errorlevel 1 (
    echo ERROR: Failed to install backend dependencies
    pause
    exit /b 1
)
echo Backend dependencies installed!
echo.

echo [Step 4/5] Installing PyInstaller...
call %POETRY_CMD% add pyinstaller --group dev
if errorlevel 1 (
    echo Warning: PyInstaller may already be installed
)
echo.

echo [Step 5/5] Building executable...
echo This may take 5-10 minutes...
call %POETRY_CMD% run pyinstaller ..\EngiCalc.spec --clean
if errorlevel 1 (
    echo ERROR: Failed to build executable
    cd ..
    pause
    exit /b 1
)
cd ..
echo.

echo ================================================
echo Build Complete!
echo ================================================
echo.
echo Your executable is located at:
echo   backend\dist\EngiCalc.exe
echo.
echo File size:
cd backend
dir dist\EngiCalc.exe | find "EngiCalc.exe"
cd ..
echo.
echo You can now copy EngiCalc.exe to your Windows desktop
echo and run it by double-clicking!
echo.
pause
