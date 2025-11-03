@echo off
chcp 65001 > nul
title ByBit Trading Bot Pro

echo ===============================================
echo    ByBit Trading Bot Pro - Запуск
echo ===============================================
echo.

echo Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не установлен!
    echo Скачайте с python.org и добавьте в PATH
    pause
    exit /b 1
)

echo Python обнаружен
python --version

echo.
echo Проверка виртуального окружения...
if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo Проверка зависимостей...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo Установка основных пакетов...
    pip install fastapi uvicorn pybit python-dotenv pydantic jinja2 aiofiles pandas numpy websockets aiohttp requests
)

echo.
echo Создание структуры папок...
mkdir api 2>nul
mkdir config 2>nul
mkdir models 2>nul
mkdir static 2>nul
mkdir templates 2>nul
mkdir data 2>nul

echo.
echo ===============================================
echo        ЗАПУСК СЕРВЕРА
echo ===============================================
echo.
echo Приложение доступно: http://localhost:8000
echo Документация API: http://localhost:8000/docs
echo.
echo Для остановки: Ctrl+C
echo.

python main.py

pause