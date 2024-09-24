@echo off
setlocal

REM Define Python installer URL and installation path
set "PYTHON_URL=https://www.python.org/ftp/python/3.10.9/python-3.10.9-amd64.exe"
set "INSTALLER=python-installer.exe"
set "INSTALL_PATH=C:\Python310"

REM Download the Python installer
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri %PYTHON_URL% -OutFile %INSTALLER%"

REM Run the installer silently
echo Installing Python...
start /wait %INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 TargetDir=%INSTALL_PATH%

REM Check if Python was installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python installation failed.
    exit /b
)

echo Python installed successfully.

REM Ask the user if they want to uninstall Python
set /p UNINSTALL="Do you want to uninstall Python? (y/n): "
if /i "%UNINSTALL%"=="y" (
    echo Uninstalling Python...
    start /wait "%INSTALL_PATH%\uninstall.exe" /quiet
    echo Python uninstalled.
) else (
    echo Python installation complete. You can uninstall it later from Control Panel.
)

REM Clean up
del %INSTALLER%

endlocal
