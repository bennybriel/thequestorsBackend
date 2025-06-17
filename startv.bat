@echo off
echo Activating virtual environment...
call .\vcareer\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)
cd careerproject
echo Virtual environment activated successfully.
@echo off
echo Starting server on port 8000...
python manage.py runserver 8000
pause