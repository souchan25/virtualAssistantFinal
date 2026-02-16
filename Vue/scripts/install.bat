@echo off
REM Vue.js Frontend Installation Script for CPSU Health Assistant (Windows)

echo ===================================================
echo CPSU Health Assistant - Vue.js Frontend Setup
echo ===================================================
echo.

REM Check if package.json exists
if not exist "package.json" (
    echo [ERROR] package.json not found
    echo Please run this script from the Vue\ directory
    pause
    exit /b 1
)

echo [OK] Found package.json
echo.

REM Check Node.js
echo Checking Node.js version...
where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Node.js is not installed
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%a in ('node -v') do set NODE_VERSION=%%a
echo [OK] Node.js %NODE_VERSION% detected
echo.

REM Check npm
echo Checking npm...
where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] npm is not installed
    pause
    exit /b 1
)

for /f "tokens=*" %%a in ('npm -v') do set NPM_VERSION=%%a
echo [OK] npm %NPM_VERSION% detected
echo.

REM Check Django backend
echo Checking Django backend...
curl -s http://localhost:8000/api/ >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [OK] Django backend is running on http://localhost:8000
) else (
    echo [WARNING] Django backend is NOT running
    echo           Start it with: cd ..\Django ^&^& python manage.py runserver
    echo           Continuing anyway...
)
echo.

REM Check .env file
echo Checking .env file...
if exist ".env" (
    echo [OK] .env file found
    type .env
) else (
    echo [WARNING] .env file not found
    echo Creating default .env file...
    (
        echo # Django Backend API
        echo VITE_API_BASE_URL=http://localhost:8000/api
        echo.
        echo # Rasa Chatbot (optional^)
        echo VITE_RASA_URL=http://localhost:5005
        echo.
        echo # App Configuration
        echo VITE_APP_NAME=CPSU Health Assistant
        echo VITE_APP_VERSION=1.0.0
    ) > .env
    echo [OK] Created .env file
)
echo.

REM Install dependencies
echo ===================================================
echo Installing npm packages...
echo This may take a few minutes...
echo ===================================================
echo.

call npm install

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ===================================================
    echo [SUCCESS] All packages installed successfully!
    echo ===================================================
) else (
    echo.
    echo [ERROR] Package installation failed
    pause
    exit /b 1
)

echo.
echo ===================================================
echo Setup Complete!
echo ===================================================
echo.
echo Next steps:
echo.
echo 1. Start Django backend (if not running^):
echo    cd ..\Django ^&^& python manage.py runserver
echo.
echo 2. Start Vue.js development server:
echo    npm run dev
echo.
echo 3. Open browser:
echo    http://localhost:5173
echo.
echo 4. Register a test account and explore!
echo.
echo Documentation:
echo    - README.md     - Complete documentation
echo    - SETUP.md      - Setup guide
echo    - COMPLETE.md   - What's been built
echo.
echo Happy coding!
echo.
pause
