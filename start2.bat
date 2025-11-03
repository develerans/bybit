@echo off
chcp 65001 > nul
title ByBit Trading Bot Pro - Запуск

echo ===============================================
echo    ByBit Trading Bot Pro - Запуск системы
echo ===============================================
echo.

echo Проверка установки Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не установлен или не добавлен в PATH
    echo Установите Python с официального сайта: https://python.org
    pause
    exit /b 1
)

echo Python обнаружен: 
python --version

echo.
echo Проверка виртуального окружения...
if not exist "venv" (
    echo Создание виртуального окружения...
    python -m venv venv
    if errorlevel 1 (
        echo ОШИБКА: Не удалось создать виртуальное окружение
        pause
        exit /b 1
    )
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo.
echo Проверка и установка зависимостей...
if exist "requirements.txt" (
    echo Обновление pip...
    python -m pip install --upgrade pip
    
    echo Установка зависимостей из requirements.txt...
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo ОШИБКА: Не удалось установить зависимости
        echo Попытка установки по отдельности...
        pip install fastapi uvicorn pybit python-dotenv pydantic jinja2 aiofiles pandas numpy websockets aiohttp requests
    )
) else (
    echo Файл requirements.txt не найден, установка основных зависимостей...
    pip install fastapi uvicorn pybit python-dotenv pydantic jinja2 aiofiles pandas numpy websockets aiohttp requests
)

echo.
echo Проверка структуры проекта...
if not exist "api" mkdir api
if not exist "config" mkdir config
if not exist "models" mkdir models
if not exist "static\css" mkdir static\css
if not exist "static\js" mkdir static\js
if not exist "templates" mkdir templates
if not exist "data\backups" mkdir data\backups
if not exist "data\exports" mkdir data\exports
if not exist "data\logs" mkdir data\logs

echo.
echo Проверка необходимых файлов...
if not exist ".env" (
    echo ВНИМАНИЕ: Файл .env не найден!
    echo Создание базового файла .env...
    (
        echo # ByBit API Keys - ПОЛУЧИТЕ НА testnet.bybit.com
        echo BYBIT_API_KEY=your_testnet_api_key_here
        echo BYBIT_API_SECRET=your_testnet_api_secret_here
        echo.
        echo # Trading Settings
        echo TESTNET=True
        echo DEFAULT_LEVERAGE=10
        echo RISK_PER_TRADE=0.02
        echo MAX_OPEN_POSITIONS=5
        echo DAILY_LOSS_LIMIT=100.0
        echo GLOBAL_STOP_LOSS=5.0
        echo.
        echo # Strategy Settings
        echo ENABLE_GRID_STRATEGY=True
        echo ENABLE_MEAN_REVERSION=True
        echo ENABLE_MOMENTUM=False
        echo GRID_LEVELS=5
        echo GRID_SPACING=0.01
        echo.
        echo # Risk Management
        echo ENABLE_TRAILING_STOP=False
        echo TRAILING_STOP_DISTANCE=1.0
        echo TAKE_PROFIT_RATIO=2.0
        echo.
        echo # Notifications
        echo ENABLE_TELEGRAM_NOTIFICATIONS=False
        echo TELEGRAM_BOT_TOKEN=your_telegram_bot_token
        echo TELEGRAM_CHAT_ID=your_telegram_chat_id
        echo.
        echo # App Settings
        echo DEBUG=True
        echo LOG_LEVEL=INFO
        echo AUTO_RESTART=True
    ) > .env
    echo Файл .env создан. Пожалуйста, настройте API ключи перед запуском!
)

echo.
echo ===============================================
echo        ЗАПУСК ТОРГОВОГО БОТА
echo ===============================================
echo.
echo Приложение будет доступно по адресу:
echo http://localhost:8000
echo.
echo API документация:
echo http://localhost:8000/docs
echo.
echo Для остановки нажмите Ctrl+C
echo.

timeout /t 3 /nobreak >nul

echo Запуск сервера...
python main.py

pause