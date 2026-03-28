@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "SCRIPT=%SCRIPT_DIR%hcs_theme_editor.py"

if not exist "%SCRIPT%" (
    echo Could not find hcs_theme_editor.py next to this launcher.
    pause
    exit /b 1
)

if defined HCS_THEME_EDITOR_PYTHON if exist "%HCS_THEME_EDITOR_PYTHON%" (
    "%HCS_THEME_EDITOR_PYTHON%" "%SCRIPT%" %*
    exit /b %errorlevel%
)

if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    "%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT%" %*
    exit /b %errorlevel%
)

where py >nul 2>nul
if %errorlevel%==0 (
    py -3 "%SCRIPT%" %*
    exit /b %errorlevel%
)

where python >nul 2>nul
if %errorlevel%==0 (
    python "%SCRIPT%" %*
    exit /b %errorlevel%
)

where python3 >nul 2>nul
if %errorlevel%==0 (
    python3 "%SCRIPT%" %*
    exit /b %errorlevel%
)

echo Python 3 was not found.
echo Install Python 3, or set HCS_THEME_EDITOR_PYTHON to a Python executable path.
pause
exit /b 1
