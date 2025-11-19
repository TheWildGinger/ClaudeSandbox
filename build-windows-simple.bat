@echo off
REM Simple build script for EngiCalc.exe (without Poetry)
REM This script uses pip directly instead of Poetry

echo ================================================
echo Building EngiCalc Standalone Executable (Simple)
echo ================================================
echo.
echo This build method uses pip directly (no Poetry needed)
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [Step 1/4] Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists, using it...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo.

echo [Step 2/4] Installing Python dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] pint handcalcs python-frontmatter markdown-it-py jinja2 python-multipart aiofiles pydantic pydantic-settings websockets pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo.

echo [Step 3/4] Building frontend...
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

echo [Step 4/4] Building executable with PyInstaller...
echo This may take 5-10 minutes...
cd backend
..\venv\Scripts\pyinstaller.exe ..\EngiCalc.spec --clean
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
echo Note: The virtual environment (venv folder) can be deleted after the build.
echo.
pause
