@echo off
echo =============================================
echo  Infinity Translator Desktop Build Script
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found: 
python --version

REM Check if required packages are installed
echo.
echo Checking dependencies...
python -c "import PySide6" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install -r requirements.txt pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK

REM Run the build script
echo.
echo Starting build process...
python build_desktop.py %*

if %errorlevel% equ 0 (
    echo.
    echo =============================================
    echo  Build completed successfully!
    echo =============================================
    echo.
    echo Your application is ready in the dist/ folder
    echo.
    if exist "dist\InfinityTranslator.exe" (
        echo Executable: dist\InfinityTranslator.exe
    )
    if exist "dist\InfinityTranslator_Package" (
        echo Distribution package: dist\InfinityTranslator_Package\
    )
    echo.
    echo Next steps:
    echo 1. Copy .env.example to .env
    echo 2. Add your API keys to .env
    echo 3. Run the executable
    echo.
) else (
    echo.
    echo =============================================
    echo  Build failed!
    echo =============================================
    echo Please check the error messages above
)

pause