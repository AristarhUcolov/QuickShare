@echo off
chcp 65001 >nul
title LAN File Share Pro - Server
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              🌐 LAN FILE SHARE PRO - SERVER                    ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Запуск веб-сервера...
echo.

python server.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска!
    echo Убедитесь что установлены зависимости: install.bat
    echo.
    pause
)
