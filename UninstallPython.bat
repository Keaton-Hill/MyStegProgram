@echo off
setlocal

REM Check if Python is installed
echo Checking for installed versions of Python...
wmic product where "name like 'Python%'" get name, version

REM Prompt user for confirmation
set /p CONFIRM="Do you want to uninstall Python? (y/n): "
if /i "%CONFIRM%" neq "y" (
    echo Uninstallation canceled.
    exit /b 0
)

REM Uninstall Python
echo Uninstalling Python...
wmic product where "name like 'Python%'" call uninstall /nointeractive

if %errorlevel% neq 0 (
    echo Failed to uninstall Python. Please check if it's installed or if you have permission.
    exit /b 1
)

echo Python has been uninstalled successfully.

endlocal
