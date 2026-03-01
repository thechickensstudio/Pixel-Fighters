@echo off

REM Setup script for Smash Fighter game (Windows)

echo Setting up Smash Fighter...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment and install dependencies
echo Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To run the game:
echo   1. Activate the virtual environment: venv\Scripts\activate.bat
echo   2. Run the game: python main.py
echo   3. When done, deactivate: deactivate
echo.
pause
