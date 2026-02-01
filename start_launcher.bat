@echo off
chcp 65001 >nul
title LAN File Share Pro - GUI Launcher
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              🚀 LAN FILE SHARE PRO - LAUNCHER                  ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Запуск GUI приложения...
echo.

python launcher.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка запуска!
    echo Убедитесь что установлены зависимости: install.bat
    echo.
    pause
)
