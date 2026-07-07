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

:: Auto Git upload
echo Auto-committing and pushing updates to GitHub...
git add .
git commit -m "Auto-sync conversation history: %date% %time%"
git push
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [WARNING] Git push failed. You may need to authenticate or check your network.
) else (
    echo.
    echo [SUCCESS] Successfully pushed updates to GitHub!
)

echo.
echo Opening Dashboard in your browser...
start "" "%~dp0dashboard\index.html"
echo.
pause
