@echo off
setlocal

:: Define the URL for the Python installer
set "python_url=https://www.python.org/ftp/python/3.10.10/python-3.10.10-amd64.exe"

:: Set the filename for the installer
set "installer=python.exe"

:: Download Python installer using PowerShell
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri '%python_url%' -OutFile '%~dp0%installer%'"

:: Check if the download was successful
if exist "%~dp0%installer%" (
    echo Download completed.
    echo Installing Python...
    :: Run the installer (silent mode)
    start /wait "" "%~dp0%installer%" /quiet InstallAllUsers=1 PrependPath=1

    echo Python installation completed.
) else (
    echo Download failed.
)

endlocal
pause
