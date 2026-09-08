@echo off
setlocal

set "PROJECT_DIR=%~dp0"

cd /d "%PROJECT_DIR%"

if not exist "%PROJECT_DIR%api\main.py" (
    echo [ERRO] Nao foi possivel localizar o projeto em:
    echo %PROJECT_DIR%
    pause
    exit /b 1
)

echo ========================================
echo       INVENTARIO DE TI
echo ========================================
echo.

echo Iniciando FastAPI...
start "FastAPI - Inventario TI" /D "%PROJECT_DIR%" cmd /k "python -m uvicorn api.main:app --reload"

timeout /t 3 /nobreak >nul

echo Iniciando Streamlit...
start "Streamlit - Inventario TI" /D "%PROJECT_DIR%streamlit_app" cmd /k "python -m streamlit run app.py"

echo.
echo ========================================
echo API:       http://127.0.0.1:8000
echo Swagger:   http://127.0.0.1:8000/docs
echo Streamlit: http://localhost:8501
echo ========================================
echo.

endlocal
