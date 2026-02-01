@echo off
chcp 65001 >nul
title QuickShare - Build All
color 0B

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║           🚀 QUICKSHARE - BUILD EXECUTABLES                ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/2] 📦 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ❌ Error installing dependencies!
    pause
    exit /b 1
)
echo.

echo [2/2] 🔨 Building executables...
python build_all.py
if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                            ║
echo ║              ✅ BUILD COMPLETED SUCCESSFULLY!              ║
echo ║                                                            ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Check dist/ folder for:
echo   ✨ QuickShare_GUI.exe (Recommended)
echo   ⚡ QuickShare_Simple.exe
echo.
pause
