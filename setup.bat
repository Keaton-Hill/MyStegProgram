@echo off
SETLOCAL

REM Navigate to the directory of the script
cd /d "%~dp0"

REM Define the TempPython folder and the Python installer path
SET TEMP_PYTHON_DIR=%cd%\TempPython
SET PYTHON_INSTALLER=python-installer.exe

REM Create the TempPython directory
mkdir "%TEMP_PYTHON_DIR%"

REM Check if the installer is already present
IF NOT EXIST "%TEMP_PYTHON_DIR%\%PYTHON_INSTALLER%" (
    echo Downloading Python installer...
    REM Replace the URL with the actual Python installer URL
    REM curl -L -o "%TEMP_PYTHON_DIR%\%PYTHON_INSTALLER%" https://www.python.org/ftp/python/3.x.x/python-3.x.x.exe
)

REM Run the installer (modify the arguments as necessary)
echo Installing Python to %TEMP_PYTHON_DIR%...
"%TEMP_PYTHON_DIR%\%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 TargetDir="%TEMP_PYTHON_DIR%"

REM Verify the installation
where python >nul 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Python installation failed.
    exit /b 1
)

REM Set the PATH to include the TempPython installation
SET PATH=%TEMP_PYTHON_DIR%;%PATH%

REM Create a virtual environment
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate.bat

REM Install required packages
pip install -r requirements.txt

REM Run the main application
python main.py
