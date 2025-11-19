@echo off
REM Create a portable package for EngiCalc that can run on Windows without installation

echo ================================================
echo Creating EngiCalc Portable Package
echo ================================================
echo.

REM Create output directory
set OUTPUT_DIR=EngiCalc-Portable
if exist "%OUTPUT_DIR%" rmdir /s /q "%OUTPUT_DIR%"
mkdir "%OUTPUT_DIR%"

echo [Step 1/4] Building frontend...
cd frontend
call npm install
call npm run build
cd ..
echo.

echo [Step 2/4] Copying backend files...
mkdir "%OUTPUT_DIR%\backend"
xcopy /E /I /Y backend\app "%OUTPUT_DIR%\backend\app"
copy backend\pyproject.toml "%OUTPUT_DIR%\backend\"
copy backend\poetry.lock "%OUTPUT_DIR%\backend\" 2>nul
copy backend\standalone.py "%OUTPUT_DIR%\backend\"
echo.

echo [Step 3/4] Copying frontend build...
mkdir "%OUTPUT_DIR%\frontend"
xcopy /E /I /Y frontend\dist "%OUTPUT_DIR%\frontend\dist"
echo.

echo [Step 4/4] Creating launcher script...
(
echo @echo off
echo echo ================================================
echo echo Starting EngiCalc...
echo echo ================================================
echo echo.
echo echo Installing/updating dependencies...
echo cd backend
echo poetry install --no-dev
echo echo.
echo echo Starting server...
echo echo The application will open in your browser automatically.
echo echo Press Ctrl+C to stop the server when done.
echo echo.
echo poetry run python standalone.py
echo pause
) > "%OUTPUT_DIR%\Start-EngiCalc.bat"
echo.

echo ================================================
echo Portable Package Created!
echo ================================================
echo.
echo Location: %OUTPUT_DIR%
echo.
echo To use:
echo 1. Copy the entire '%OUTPUT_DIR%' folder to your Windows desktop
echo 2. Make sure Python 3.10+ and Poetry are installed
echo 3. Double-click 'Start-EngiCalc.bat' to run
echo.
echo To distribute: Zip the '%OUTPUT_DIR%' folder
echo.
pause
