@echo off
chcp 65001 >nul
echo ========================================
echo 🚀 LAN File Share Pro - Сборка
echo ========================================
echo.

echo 📦 Установка зависимостей...
pip install -r requirements.txt
echo.

echo 🔨 Запуск сборки...
python build.py
echo.

echo ✅ Готово!
echo.
pause
