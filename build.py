"""
Скрипт для сборки приложения в .exe файл
Запустите: python build.py
"""

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Получить путь к текущей директории
current_dir = Path(__file__).parent

# Очистить предыдущие сборки
for dir_name in ['build', 'dist']:
    dir_path = current_dir / dir_name
    if dir_path.exists():
        shutil.rmtree(dir_path)
        print(f"✓ Очищена папка {dir_name}")

# Параметры для PyInstaller
pyinstaller_args = [
    str(current_dir / 'launcher.py'),
    '--name=LAN_File_Share_Pro',
    '--onefile',
    '--windowed',
    '--icon=NONE',
    '--add-data=server.py;.',
    '--hidden-import=flask',
    '--hidden-import=qrcode',
    '--hidden-import=PIL',
    '--hidden-import=werkzeug',
    '--collect-all=flask',
    '--collect-all=qrcode',
    '--noconsole',
    f'--distpath={current_dir / "dist"}',
    f'--workpath={current_dir / "build"}',
    f'--specpath={current_dir}',
]

print("\n" + "="*60)
print("🚀 Начинается сборка LAN File Share Pro...")
print("="*60 + "\n")

try:
    PyInstaller.__main__.run(pyinstaller_args)
    
    print("\n" + "="*60)
    print("✅ Сборка успешно завершена!")
    print("="*60)
    print(f"\n📦 Исполняемый файл находится в: {current_dir / 'dist'}")
    print(f"📁 Файл: LAN_File_Share_Pro.exe\n")
    
except Exception as e:
    print("\n" + "="*60)
    print("❌ Ошибка при сборке:")
    print("="*60)
    print(f"\n{str(e)}\n")
