@echo off
echo ================================================
echo   Windows Optimizer - Build System v2.0
echo ================================================
echo.

REM === CONFIGURACOES - EDITE AQUI ===
set APP_NAME=WinOptimizer
set OUTPUT_DIR=..\release
set BUILD_TEMP=..\build_temp
set SPEC_DIR=..\build_temp
REM ==================================

echo [1/2] Verificando PyInstaller...
..\venv\Scripts\python.exe -m pip install pyinstaller --quiet 2>nul || (
    ..\.venv\Scripts\python.exe -m pip install pyinstaller --quiet
)

echo [2/2] Compilando %APP_NAME%.exe ...
..\.venv\Scripts\python.exe -m PyInstaller ^
    --noconfirm ^
    --onedir ^
    --windowed ^
    --uac-admin ^
    --name "%APP_NAME%" ^
    --icon="icon.ico" ^
    --distpath "%OUTPUT_DIR%" ^
    --workpath "%BUILD_TEMP%" ^
    --specpath "%SPEC_DIR%" ^
    --add-data "locales;locales" ^
    --add-data "..\scripts;scripts" ^
    "main.py"

if %errorlevel% == 0 (
    echo.
    echo ================================================
    echo  Build concluido com sucesso!
    echo  Arquivo: %OUTPUT_DIR%\%APP_NAME%\%APP_NAME%.exe
    echo ================================================
) else (
    echo.
    echo  [ERRO] O build falhou. Verifique os logs acima.
)
pause
