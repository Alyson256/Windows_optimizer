@echo off
setlocal EnableExtensions

:: ============================================================
:: 12_system_cleanup.bat — System and Network Cache Cleanup
::
:: Safely clears temporary files, network DNS cache, Windows
:: Update cache, and empties the Recycle Bin.
::
:: Requires: Administrator
:: Safe: Only removes cache and temporary files.
:: ============================================================

call "%~dp0_lib\colors.bat"
call "%~dp0_lib\require_admin.bat" || exit /b 1

echo.
echo  %CYAN%[12] System and Network Cleanup%RESET%
echo  %DIM%  Clearing temporary files, DNS cache, and system caches...%RESET%
echo.

set "CLEARED=0"

:: ── Network / DNS Cache ──────────────────────────────────────
echo  %DIM%  Flushing DNS cache...%RESET%
ipconfig /flushdns >nul 2>&1
if %errorLevel% == 0 (
    echo  %GREEN%  [+]%RESET% DNS Resolver Cache flushed
    set /a CLEARED+=1
) else (
    echo  %YELLOW%  [-]%RESET% Failed to flush DNS cache
)

:: ── User Temp Folder ─────────────────────────────────────────
echo  %DIM%  Clearing User Temp folder...%RESET%
del /q /f /s "%TEMP%\*" >nul 2>&1
for /d %%x in ("%TEMP%\*") do rd /s /q "%%x" >nul 2>&1
echo  %GREEN%  [+]%RESET% User Temp folder cleared
set /a CLEARED+=1

:: ── Windows Temp Folder ──────────────────────────────────────
echo  %DIM%  Clearing Windows Temp folder...%RESET%
del /q /f /s "C:\Windows\Temp\*" >nul 2>&1
for /d %%x in ("C:\Windows\Temp\*") do rd /s /q "%%x" >nul 2>&1
echo  %GREEN%  [+]%RESET% Windows Temp folder cleared
set /a CLEARED+=1

:: ── Windows Update Cache ─────────────────────────────────────
echo  %DIM%  Clearing Windows Update cache (SoftwareDistribution)...%RESET%
net stop wuauserv >nul 2>&1
net stop bits >nul 2>&1
del /q /f /s "C:\Windows\SoftwareDistribution\Download\*" >nul 2>&1
for /d %%x in ("C:\Windows\SoftwareDistribution\Download\*") do rd /s /q "%%x" >nul 2>&1
net start wuauserv >nul 2>&1
net start bits >nul 2>&1
echo  %GREEN%  [+]%RESET% Windows Update Download cache cleared
set /a CLEARED+=1

:: ── Recycle Bin ──────────────────────────────────────────────
echo  %DIM%  Emptying Recycle Bin...%RESET%
powershell -NonInteractive -Command "Clear-RecycleBin -Force -ErrorAction SilentlyContinue" >nul 2>&1
echo  %GREEN%  [+]%RESET% Recycle Bin emptied
set /a CLEARED+=1

echo.
echo  %CYAN%  ════════════════════════════════════════════════%RESET%
echo  %GREEN%  ✓ System cleanup completed.%RESET%
echo  %DIM%  Note: Some files in use by running apps were skipped (normal).%RESET%
echo  %CYAN%  ════════════════════════════════════════════════%RESET%
echo.

if defined LOG_FILE call "%~dp0_lib\logger.bat" "System and Network cleanup completed" "SUCCESS"
exit /b 0
