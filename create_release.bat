@echo off
echo ========================================
echo Creating GitHub Release for v1.0.0
echo ========================================
echo.
echo Tag v1.0.0 has been pushed to GitHub.
echo.
echo Opening GitHub release page in your browser...
echo.
start https://github.com/kaveinthran/NVSpeechPlayer/releases/new?tag=v1.0.0
echo.
echo ========================================
echo INSTRUCTIONS:
echo ========================================
echo.
echo 1. The GitHub release page should open in your browser
echo 2. It will have tag v1.0.0 pre-selected
echo 3. Title: nvSpeechPlayer v1.0.0 - Dual Intonation Mode
echo 4. Copy the description from RELEASE_NOTES_v1.0.0.md
echo 5. Upload file: nvSpeechPlayer_master-9d2b6eb.nvda-addon
echo 6. Check "Set as the latest release"
echo 7. Click "Publish release"
echo.
echo The addon file is located at:
echo %~dp0nvSpeechPlayer_master-9d2b6eb.nvda-addon
echo.
echo Press any key to exit...
pause >nul
