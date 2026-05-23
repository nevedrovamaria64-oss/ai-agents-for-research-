@echo off
REM Installation script for News Agent
REM Run this in Command Prompt (cmd.exe) from the project directory

echo.
echo ============================================
echo   NEWS AGENT - Setup Script
echo ============================================
echo.

REM Check Python
echo [1] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo [OK]
echo.

REM Check pip
echo [2] Checking pip installation...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip not found!
    echo Try: python -m pip --version
    pause
    exit /b 1
)

pip --version
echo [OK]
echo.

REM Install requirements
echo [3] Installing dependencies...
echo This may take a few minutes...
echo.

pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [OK]
echo.

REM Create directories
echo [4] Creating project directories...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "news_output" mkdir news_output
echo [OK]
echo.

REM Show next steps
echo ============================================
echo   Installation Complete!
echo ============================================
echo.
echo Next steps:
echo.
echo 1. Place your organizations.xlsx file in the 'data' folder
echo    (Required columns: Название, Сайт, Категории)
echo.
echo 2. Run the news agent:
echo    python main.py
echo.
echo 3. Results will be saved to 'news_output' folder
echo.
echo For more information, see README.md
echo.
pause
