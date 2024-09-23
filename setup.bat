@echo off
REM Navigate to the directory of the script
cd /d "%~dp0"

REM Create a virtual environment
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate

REM Install required packages
pip install -r requirements.txt

REM Run the main application
python main.py
