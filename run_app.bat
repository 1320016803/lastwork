@echo off
cd /d "%~dp0"
where pyw >nul 2>&1 && pyw -3 "%~dp0main.py" && exit /b 0
where pythonw >nul 2>&1 && pythonw "%~dp0main.py" && exit /b 0
py -3 "%~dp0main.py"
pause
