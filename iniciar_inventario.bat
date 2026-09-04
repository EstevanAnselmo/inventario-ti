@echo off

echo ========================================
echo       INVENTARIO DE TI
echo ========================================
echo.

echo Iniciando FastAPI...
start "FastAPI - Inventario TI" cmd /k "cd /d C:\Users\estevan-silva\Documents\inventario_ti && python -m uvicorn api.main:app --reload"

timeout /t 3 /nobreak >nul

echo Iniciando Streamlit...
start "Streamlit - Inventario TI" cmd /k "cd /d C:\Users\estevan-silva\Documents\inventario_ti\streamlit_app && python -m streamlit run app.py"

echo.
echo ========================================
echo API:       http://127.0.0.1:8000
echo Swagger:   http://127.0.0.1:8000/docs
echo Streamlit: http://localhost:8501
echo ========================================
echo.
pause