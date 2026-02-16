@echo off
REM ==========================================
REM CPSU Rasa Management Script (Windows)
REM ==========================================
REM Usage: scripts\rasa.bat [command]
REM Commands: action, main, train, shell, status

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set RASA_DIR=%PROJECT_ROOT%\Rasa
set PYTHON=%PROJECT_ROOT%\venv\Scripts\python.exe

echo ========================================
echo   CPSU Rasa Management Script
echo ========================================
echo.

REM Check if venv exists
if not exist "%PYTHON%" (
    echo ERROR: Virtual environment not found!
    echo Expected: %PYTHON%
    echo Run: python -m venv venv
    exit /b 1
)

REM Check if Rasa directory exists
if not exist "%RASA_DIR%" (
    echo ERROR: Rasa directory not found!
    exit /b 1
)

cd /d "%RASA_DIR%"

if "%1"=="" goto help
if "%1"=="action" goto action
if "%1"=="main" goto main
if "%1"=="train" goto train
if "%1"=="shell" goto shell
if "%1"=="test" goto shell
if "%1"=="status" goto status
if "%1"=="help" goto help
goto help

:action
echo Starting Rasa Action Server...
echo Port: 5055
echo.
"%PYTHON%" -m rasa run actions
goto end

:main
echo Starting Rasa Main Server...
echo Port: 5005
echo.

REM Find latest model
for /f "delims=" %%i in ('dir /b /o-d models\*.tar.gz 2^>nul') do (
    set LATEST_MODEL=%%i
    goto found_model
)
echo WARNING: No trained model found!
echo Run: scripts\rasa.bat train
exit /b 1

:found_model
echo Model: models\%LATEST_MODEL%
echo.
"%PYTHON%" -m rasa run --model "models\%LATEST_MODEL%" --enable-api --cors "*" --port 5005
goto end

:train
echo Training Rasa Model...
echo This may take a few minutes...
echo.
"%PYTHON%" -m rasa train
goto end

:shell
echo Starting Rasa Shell...
echo Type your messages to test the bot.
echo Type '/stop' to exit.
echo.
"%PYTHON%" -m rasa shell
goto end

:status
echo Checking server status...
echo.

curl -s http://localhost:5055 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Action Server (5055): RUNNING
) else (
    echo Action Server (5055): NOT RUNNING
)

curl -s http://localhost:5005 >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Main Server (5005):   RUNNING
) else (
    echo Main Server (5005):   NOT RUNNING
)

echo.
echo Trained models:
dir /b /o-d models\*.tar.gz 2>nul || echo   (none found)
goto end

:help
echo Usage: scripts\rasa.bat [command]
echo.
echo Commands:
echo   action  - Start Rasa action server (port 5055)
echo   main    - Start Rasa main server (port 5005)
echo   train   - Train Rasa model
echo   shell   - Interactive Rasa shell for testing
echo   status  - Check if servers are running
echo   help    - Show this help message
echo.
echo Examples:
echo   scripts\rasa.bat action   # Start action server
echo   scripts\rasa.bat train    # Train new model
goto end

:end
endlocal

