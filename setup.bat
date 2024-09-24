@echo off
setlocal

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/.
    exit /b 1
)

REM Install required packages from requirements.txt
if exist requirements.txt (
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo Failed to install required packages. Check for errors.
        exit /b 1
    )
) else (
    echo requirements.txt not found. Skipping package installation.
)

REM Run the main application
echo Running the Python application...
python main.py
if %errorlevel% neq 0 (
    echo Failed to run the application. Check for errors.
    exit /b 1
)

endlocal
