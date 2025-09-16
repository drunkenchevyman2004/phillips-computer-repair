@echo off
REM Batch file to run the PowerShell cleanup script with elevated privileges.
REM Author: ChatGPT (auto‑generated)

REM Attempt to detect if script is running with administrative rights.  If not,
REM re‑run itself using PowerShell to prompt for elevation.
openfiles >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges…
    powershell.exe -Command "Start-Process '%~f0' -Verb RunAs"
    goto :eof
)

REM Run the PowerShell script with ExecutionPolicy bypassed
echo Running Windows cleanup script...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0windows_cleanup.ps1"

echo.
echo Cleanup completed.  Press any key to exit.
pause >nul
