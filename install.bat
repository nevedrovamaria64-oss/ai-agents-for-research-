@echo off
REM Smart Setup Script for News Agent
REM This script will:
REM 1. Check Python installation
REM 2. Install all dependencies
REM 3. Verify installation
REM 4. Create necessary directories

setlocal enabledelayedexpansion
cd /d "%~dp0"

echo.
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          NEWS AGENT - Automatic Setup                             ║
echo ║          Новостной агент - Автоматическая установка              ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM Step 1: Check Python
echo [STEP 1] Checking Python installation...
echo          Проверка установки Python...
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo    ОШИБКА: Python не найден!
    echo.
    echo   Please install Python 3.10+ from: https://www.python.org/downloads/
    echo   Установите Python 3.10+ с: https://www.python.org/downloads/
    echo.
    echo   IMPORTANT / ВАЖНО:
    echo   ✅ Check "Add Python to PATH" during installation
    echo   ✅ Отметьте "Add Python to PATH" при установке
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Found: %PYTHON_VERSION%
echo ✓ Найдена: %PYTHON_VERSION%
echo.

REM Step 2: Check pip
echo [STEP 2] Checking pip...
echo          Проверка pip...
echo.

pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: pip not found
    echo    ОШИБКА: pip не найден
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('pip --version 2^>^&1') do set PIP_VERSION=%%i
echo ✓ %PIP_VERSION%
echo.

REM Step 3: Create directories
echo [STEP 3] Creating project directories...
echo          Создание директорий проекта...
echo.

if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "news_output" mkdir news_output

echo ✓ data/
echo ✓ logs/
echo ✓ news_output/
echo.

REM Step 4: Install dependencies
echo [STEP 4] Installing dependencies (this may take 2-5 minutes)...
echo          Установка зависимостей (может занять 2-5 минут)...
echo.

pip install --upgrade pip >nul 2>&1

REM Install with progress
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ❌ ERROR: Failed to install dependencies
    echo    ОШИБКА: Не удалось установить зависимости
    echo.
    echo Try manually: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ All dependencies installed successfully
echo ✓ Все зависимости установлены успешно
echo.

REM Step 5: Verify installation
echo [STEP 5] Verifying installation...
echo          Проверка установки...
echo.

python test_setup.py

echo.
echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║          ✅ SETUP COMPLETE / УСТАНОВКА ЗАВЕРШЕНА                  ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo NEXT STEPS / СЛЕДУЮЩИЕ ШАГИ:
echo.
echo 1. Create data\organizations.xlsx with your organizations
echo    Создайте data\organizations.xlsx с вашими организациями
echo.
echo 2. Run the agent:
echo    python main.py
echo.
echo For more info, see: README.md or SETUP_GUIDE.md
echo Для подробнее смотрите: README.md или SETUP_GUIDE.md
echo.
pause
