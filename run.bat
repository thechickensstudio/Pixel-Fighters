@echo off

REM Quick run script for Smash Fighter game (Windows)

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment and run game
call venv\Scripts\activate.bat
python main.py
deactivate
