@echo off

set "ENV_NAME=IoTStudioENV"

:: Create the virtual environment
echo Creating virtual environment in %ENV_NAME%...
python -m venv %ENV_NAME%

:: Activate the virtual environment
echo Activating virtual environment...
call "%ENV_NAME%\Scripts\activate.bat"

:: Confirm activation
if "%VIRTUAL_ENV%" neq "" (
    echo Virtual environment activated: %VIRTUAL_ENV%
) else (
    echo Failed to activate the virtual environment.
    pause
    exit /b
)

:: Keep the terminal open
echo Virtual environment setup is complete. You can now install dependencies using pip.
pause
