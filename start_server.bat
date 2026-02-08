@echo off
echo Starting Email Triage Assistant Server...
echo Optimized for Production (Waitress)
echo -----------------------------------

:: Activate virtual env if exists
if exist ..\.venv\Scripts\activate call ..\.venv\Scripts\activate
if exist ..\venv\Scripts\activate call ..\venv\Scripts\activate

:: Navigate to backend to ensure imports work correctly
cd backend

:: Start Waitress Server
echo [INFO] Server listening on http://127.0.0.1:5000
waitress-serve --listen=127.0.0.1:5000 --call app:app

pause
