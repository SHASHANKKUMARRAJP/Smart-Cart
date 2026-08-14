@echo off
echo ===============================================
echo Starting Smart Cart Price Comparison Platform...
echo ===============================================
echo.

:: Start the default web browser to open the local URL in the background
start "" http://127.0.0.1:5000

:: Run the Flask server using the virtual environment python interpreter
.\.venv\Scripts\python.exe run.py

if %errorlevel% neq 0 (
    echo.
    echo Server stopped with error or could not start.
    pause
)
