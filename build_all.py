"""
Build script for QuickShare - Creates executable versions
Скрипт сборки QuickShare - Создаёт исполняемые версии
"""

import PyInstaller.__main__
import os
import shutil
from pathlib import Path

# Get current directory
current_dir = Path(__file__).parent

print("\n" + "="*70)
print("🚀 QUICKSHARE - BUILDING EXECUTABLES")
print("="*70 + "\n")

# Clean previous builds
for dir_name in ['build', 'dist']:
    dir_path = current_dir / dir_name
    if dir_path.exists():
        shutil.rmtree(dir_path)
        print(f"✓ Cleaned {dir_name}/")

os.makedirs(current_dir / 'dist', exist_ok=True)

# Build 1: GUI Launcher (Recommended)
print("\n" + "="*70)
print("📦 Building GUI Version...")
print("="*70)

separator = ';' if os.name == 'nt' else ':'
PyInstaller.__main__.run([
    str(current_dir / 'launcher.py'),
    '--name=QuickShare_GUI',
    '--onefile',
    '--windowed',
    f'--add-data=server.py{separator}.',
    f'--add-data=translations.py{separator}.',
    '--hidden-import=flask',
    '--hidden-import=qrcode',
    '--hidden-import=PIL',
    '--hidden-import=werkzeug',
    '--hidden-import=jinja2',
    '--collect-all=flask',
    '--collect-all=qrcode',
    '--collect-data=flask',
    '--noconsole',
    f'--distpath={current_dir / "dist"}',
    f'--workpath={current_dir / "build"}',
    f'--specpath={current_dir}',
])

print("\n✅ GUI version built successfully!")

# Build 2: Simple CMD Version
print("\n" + "="*70)
print("📦 Building Simple CMD Version...")
print("="*70)

PyInstaller.__main__.run([
    str(current_dir / 'server_simple_cmd_version.py'),
    '--name=QuickShare_Simple',
    '--onefile',
    '--console',
    '--hidden-import=flask',
    '--hidden-import=werkzeug',
    '--collect-all=flask',
    f'--distpath={current_dir / "dist"}',
    f'--workpath={current_dir / "build"}',
    f'--specpath={current_dir}',
])

print("\n✅ Simple version built successfully!")

# Summary
print("\n" + "="*70)
print("✅ BUILD COMPLETED SUCCESSFULLY!")
print("="*70)
print(f"\n📦 Executables are in: {current_dir / 'dist'}\n")
print("━" * 70)
print("  Files created:")
print("  ✨ QuickShare_GUI.exe     - Full GUI (Recommended)")
print("  ⚡ QuickShare_Simple.exe  - Lightweight CMD")
print("━" * 70)
print("\n💡 Tip: Use QuickShare_GUI.exe for the best experience!")
print("\n" + "="*70 + "\n")
