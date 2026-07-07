@echo off
echo ===================================================
echo   Antigravity Conversation History Synchronizer
echo ===================================================
echo.

:: Run Python script
echo Running python parser...
python "%~dp0scripts\extract_history.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Python script failed. Please make sure Python is installed and configured.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo Sync completed successfully!
echo.
echo Opening Dashboard in your browser...
start "" "%~dp0dashboard\index.html"
echo.
echo If you have initialized Git, you can push changes by running:
echo git add .
echo git commit -m "Sync conversation history"
echo git push
echo.
pause
