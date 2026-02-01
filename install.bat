@echo off
chcp 65001 >nul
title LAN File Share Pro - Установка
color 0A

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║         🚀 LAN FILE SHARE PRO - УСТАНОВКА ЗАВИСИМОСТЕЙ        ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.

echo [1/2] 📦 Проверка Python...
python --version
if errorlevel 1 (
    echo.
    echo ❌ Python не найден!
    echo Установите Python с https://www.python.org/downloads/
    echo.
    pause
    exit
)
echo ✓ Python установлен
echo.

echo [2/2] 📥 Установка зависимостей...
echo.
pip install -r requirements.txt
echo.

if errorlevel 1 (
    echo.
    echo ❌ Ошибка установки зависимостей
    echo.
    pause
    exit
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              ✅ УСТАНОВКА УСПЕШНО ЗАВЕРШЕНА!                   ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Теперь вы можете:
echo.
echo   1. Запустить GUI: start_launcher.bat
echo   2. Запустить сервер: start_server.bat
echo   3. Собрать .exe: build_simple.bat
echo.
pause
