<div align="center">

# 🚀 QuickShare - LAN File Transfer

### *Быстрая передача файлов в локальной сети / Fast Local Network File Sharing*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
![Version](https://img.shields.io/badge/version-2.0-purple)
![Languages](https://img.shields.io/badge/languages-EN%20%7C%20RU-blue)

**Мощное приложение для обмена файлами с красивым интерфейсом**  
**Powerful file sharing application with beautiful interface**

[📥 Download .exe](#-download) | [🚀 Quick Start](#-quick-start-english) | [📖 Documentation](#documentation)

</div>

---

## 📑 Table of Contents / Содержание

- [English Documentation](#-english-documentation) 🇬🇧
- [Русская Документация](#-русская-документация) 🇷🇺

---

<div id="english-documentation"></div>

# 🇬🇧 ENGLISH DOCUMENTATION

## ✨ Features

### 🎨 Beautiful Modern Interface
- **Dark gradient theme** with smooth animations
- **Responsive design** - works on all devices
- **Intuitive UX** - easy to use for everyone
- **Real-time updates** - instant feedback

### 📤 Upload Made Easy
- **🎯 Drag & Drop** - Just drag files into browser
- **📁 Multiple files** - Upload many files at once
- **📂 Folder upload** - Upload entire folders with structure
- **📊 Progress bar** - Watch your upload progress in real-time
- **💪 Large files** - Support up to 500 MB per file

### 📥 Download & Share
- **⬇️ Direct download** - One-click file download
- **🗜️ Auto-ZIP folders** - Folders automatically compressed
- **⚡ Fast transfer** - Optimized for speed

### 🔧 Smart Features
- **🔍 Instant search** - Find files quickly
- **📊 Smart sorting** - By name, size, or date
- **🗑️ Easy delete** - Remove files with confirmation
- **📋 File info** - Size, date, and metadata
- **📱 QR Code** - Quick mobile access
- **📈 Statistics** - Total files and storage used
- **🌍 Multi-language** - English & Russian interfaces

### 💻 Professional Tools
- **🖥️ GUI Launcher** - Beautiful desktop application
- **⚙️ Easy setup** - Configure port and folders
- **📡 Network info** - Shows local IP automatically
- **🎨 QR display** - Built-in QR code viewer
- **🌐 Browser button** - Open in browser instantly

---

## 📥 Download

### Option 1: Pre-built Executables (Recommended)
After building, you'll get:
- **QuickShare_GUI.exe** - ⭐ Full GUI application (Recommended)
- **QuickShare_Simple.exe** - Lightweight command-line version

### Option 2: Run from Source
Requires Python 3.7+

---

## 🚀 Quick Start (English)

### For Windows Users (Easiest):

1. **Install Python** (if not installed):
   - Download from [python.org](https://www.python.org/downloads/)
   - ✅ Check "Add to PATH" during installation

2. **Double-click**: `install.bat`
   - Installs all required packages

3. **Double-click**: `start_launcher.bat`
   - Opens the GUI application

4. **Click** "Start Server"

5. **Open browser** or scan QR code from your phone!

### For Python Users:

```bash
# Install dependencies
pip install -r requirements.txt

# Launch GUI
python launcher.py

# OR launch server directly
python server.py
```

### Build Your Own .exe:

```bash
# Install dependencies
pip install -r requirements.txt

# Build all versions
python build_all.py
```

Find your .exe files in the `dist/` folder!

---

## 🎯 How to Use

### Basic Usage:

1. **Start the server** (GUI or command-line)
2. **Note the URL** displayed (e.g., `http://192.168.1.5:8000`)
3. **Open browser** on any device in your network
4. **Upload/Download** files easily!

### From Mobile Phone:

1. Connect phone to **same WiFi** as computer
2. **Scan QR code** shown in the app
3. Browser opens automatically!
4. Upload photos/files directly

### Switch Language:

- Click the **🌐 button** in the web interface
- Choose between English and Russian
- Language preference saved for 30 days

---

## 🌐 Network Access

All devices on your **local network** can access:

- **Computer**: `http://192.168.X.X:8000`
- **Mobile**: Scan the QR code
- **Same WiFi**: Required for all devices

---

## 📁 Project Structure

```
QuickShare/
├── 📱 GUI Version
│   ├── launcher.py              - Desktop GUI application
│   └── server.py                - Full-featured web server
│
├── 💻 Simple Version
│   └── server_simple_cmd_version.py - Command-line server
│
├── 🌍 Translations
│   └── translations.py          - Language support (EN/RU)
│
├── 🔨 Build Tools
│   ├── build_all.py             - Build all .exe versions
│   ├── build_all.bat            - Quick build script
│   └── requirements.txt         - Python dependencies
│
├── 🚀 Launch Scripts
│   ├── install.bat              - Install dependencies
│   ├── start_launcher.bat       - Start GUI
│   └── start_server.bat         - Start server
│
└── 📂 uploads/                  - Uploaded files storage
```

---

## 🛠️ Technologies

| Category | Technology |
|----------|-----------|
| **Backend** | Flask (Python web framework) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Desktop GUI** | Tkinter (Python built-in) |
| **QR Codes** | python-qrcode + Pillow |
| **Packaging** | PyInstaller |
| **i18n** | Custom translation system |

---

## 🔐 Security Notes

⚠️ **Important Security Information:**

- ✅ **Safe**: Use in trusted local networks (home, office)
- ❌ **Unsafe**: Do NOT expose to internet without security
- 🔒 **Features**: File size limits, path validation
- 🏠 **Recommended**: Local network only

**This is for local file sharing, not a production web server!**

---

## 💡 Use Cases

### 1. Photo Transfer (Phone → PC)
- Launch server on PC
- Scan QR with phone
- Upload photos instantly
- ✅ Done in seconds!

### 2. File Sharing (Office/Home)
- One person runs server
- Everyone connects via IP
- Upload/download freely
- ✅ No email attachments needed!

### 3. Backup Folders
- Drag folder into browser
- Full structure uploaded
- Download as ZIP anytime
- ✅ Easy backups!

---

## 🎨 Interface Preview

### Web Interface Features:
- 🌙 **Dark theme** with purple gradients
- 🎯 **Drag & Drop** upload zone
- 📊 **Progress indicators** for uploads
- 🔍 **Search bar** with instant filtering
- 📱 **Mobile responsive** design
- 🌐 **Language toggle** (EN/RU)

### GUI Launcher Features:
- 🖥️ **Modern dark interface**
- ▶️ **One-click** start/stop
- ⚙️ **Settings panel** (port, folder)
- 📡 **Network info** display
- 📱 **QR code** built-in
- 🌐 **Browser button**

---

## 🆚 Version Comparison

| Feature | Simple CMD | Full GUI |
|---------|:----------:|:--------:|
| Beautiful Web UI | ✅ | ✅ |
| Drag & Drop | ❌ | ✅ |
| Folder Upload | ❌ | ✅ |
| Search & Sort | ❌ | ✅ |
| Delete Files | ❌ | ✅ |
| Progress Bar | ❌ | ✅ |
| QR Code | ❌ | ✅ |
| GUI Launcher | ❌ | ✅ |
| Multi-language | ❌ | ✅ |
| File Size | ~5 MB | ~15 MB |

**Recommendation**: Use **GUI version** for best experience!

---

## 📋 Requirements

### Minimum:
- **OS**: Windows 7+, Linux, macOS
- **Python**: 3.7 or higher
- **RAM**: 100 MB
- **Disk**: 50 MB

### Dependencies (auto-installed):
```
Flask==3.0.0
qrcode==7.4.2
Pillow==10.1.0
pyinstaller==6.3.0  # Only for building .exe
```

---

## 🤝 Contributing

Contributions welcome! You can:
- 🐛 Report bugs
- 💡 Suggest features
- 🌍 Add translations
- 📝 Improve docs
- 🔧 Submit pull requests

---

## 📄 License

**MIT License** - Free to use for any purpose!

See [LICENSE](LICENSE) file for details.

---

## 🎉 Changelog

### Version 2.0 (Current)
- ✨ Complete UI redesign
- 🌍 Multi-language support (EN/RU)
- 📤 Drag & Drop upload
- 📁 Folder support with ZIP
- 🖥️ Professional GUI launcher
- 📱 QR code generation
- 🔍 Search & sort features
- 📦 Multiple .exe builds

### Version 1.0 (Legacy)
- Basic file upload/download
- Simple list interface
- Local network access

---

## 📞 Support

Having issues? Check:
1. [Documentation](#documentation)
2. [Common Issues](#common-issues)
3. Open an issue on GitHub

---

## 🙏 Acknowledgments

Built with ❤️ using:
- **Flask** - Web framework
- **Python** - Programming language
- **Tkinter** - GUI framework
- Open source community

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ | [Report Bug](../../issues) | [Request Feature](../../issues)

</div>

---
---

<div id="русская-документация"></div>

# 🇷🇺 РУССКАЯ ДОКУМЕНТАЦИЯ

## ✨ Возможности

### 🎨 Красивый Современный Интерфейс
- **Темная тема** с градиентами и плавными анимациями
- **Адаптивный дизайн** - работает на всех устройствах
- **Интуитивный UX** - легко использовать каждому
- **Обновления в реальном времени** - мгновенная обратная связь

### 📤 Простая Загрузка
- **🎯 Drag & Drop** - Просто перетащите файлы в браузер
- **📁 Множественная загрузка** - Загружайте много файлов сразу
- **📂 Загрузка папок** - Загружайте целые папки со структурой
- **📊 Прогресс-бар** - Следите за процессом загрузки
- **💪 Большие файлы** - Поддержка до 500 МБ на файл

### 📥 Скачивание и Обмен
- **⬇️ Прямое скачивание** - Скачивание в один клик
- **🗜️ Авто-ZIP для папок** - Папки автоматически архивируются
- **⚡ Быстрая передача** - Оптимизировано для скорости

### 🔧 Умные Функции
- **🔍 Мгновенный поиск** - Находите файлы быстро
- **📊 Умная сортировка** - По имени, размеру или дате
- **🗑️ Легкое удаление** - Удаление с подтверждением
- **📋 Информация о файлах** - Размер, дата и метаданные
- **📱 QR-код** - Быстрый доступ с мобильных
- **📈 Статистика** - Общее количество файлов и размер
- **🌍 Мультиязычность** - Английский и русский интерфейсы

### 💻 Профессиональные Инструменты
- **🖥️ GUI Launcher** - Красивое desktop приложение
- **⚙️ Легкая настройка** - Настройка порта и папок
- **📡 Сетевая информация** - Автоматически показывает локальный IP
- **🎨 Отображение QR** - Встроенный просмотрщик QR-кодов
- **🌐 Кнопка браузера** - Мгновенное открытие в браузере

---

## 📥 Скачать

### Вариант 1: Готовые исполняемые файлы (Рекомендуется)
После сборки вы получите:
- **QuickShare_GUI.exe** - ⭐ Полное GUI приложение (Рекомендуется)
- **QuickShare_Simple.exe** - Облегченная консольная версия

### Вариант 2: Запуск из исходников
Требуется Python 3.7+

---

## 🚀 Быстрый Старт (Русский)

### Для пользователей Windows (Проще всего):

1. **Установите Python** (если не установлен):
   - Скачайте с [python.org](https://www.python.org/downloads/)
   - ✅ Отметьте "Add to PATH" при установке

2. **Дважды кликните**: `install.bat`
   - Установит все необходимые пакеты

3. **Дважды кликните**: `start_launcher.bat`
   - Откроет GUI приложение

4. **Нажмите** "Запустить сервер"

5. **Откройте браузер** или отсканируйте QR-код с телефона!

### Для Python пользователей:

```bash
# Установить зависимости
pip install -r requirements.txt

# Запустить GUI
python launcher.py

# ИЛИ запустить сервер напрямую
python server.py
```

### Собрать свой .exe:

```bash
# Установить зависимости
pip install -r requirements.txt

# Собрать все версии
python build_all.py
```

Найдите .exe файлы в папке `dist/`!

---

## 🎯 Как Использовать

### Базовое использование:

1. **Запустите сервер** (GUI или командная строка)
2. **Запомните URL** который отображается (например `http://192.168.1.5:8000`)
3. **Откройте браузер** на любом устройстве в вашей сети
4. **Загружайте/Скачивайте** файлы легко!

### С мобильного телефона:

1. Подключите телефон к **той же WiFi** что и компьютер
2. **Отсканируйте QR-код** показанный в приложении
3. Браузер откроется автоматически!
4. Загружайте фото/файлы напрямую

### Переключить язык:

- Нажмите **кнопку 🌐** в веб-интерфейсе
- Выберите между английским и русским
- Язык сохраняется на 30 дней

---

## 🌐 Доступ из Сети

Все устройства в вашей **локальной сети** могут получить доступ:

- **Компьютер**: `http://192.168.X.X:8000`
- **Мобильный**: Отсканируйте QR-код
- **Та же WiFi**: Требуется для всех устройств

---

## 📁 Структура Проекта

```
QuickShare/
├── 📱 GUI Версия
│   ├── launcher.py              - Desktop GUI приложение
│   └── server.py                - Полнофункциональный веб-сервер
│
├── 💻 Простая Версия
│   └── server_simple_cmd_version.py - Консольный сервер
│
├── 🌍 Переводы
│   └── translations.py          - Поддержка языков (EN/RU)
│
├── 🔨 Инструменты Сборки
│   ├── build_all.py             - Сборка всех .exe версий
│   ├── build_all.bat            - Скрипт быстрой сборки
│   └── requirements.txt         - Python зависимости
│
├── 🚀 Скрипты Запуска
│   ├── install.bat              - Установка зависимостей
│   ├── start_launcher.bat       - Запуск GUI
│   └── start_server.bat         - Запуск сервера
│
└── 📂 uploads/                  - Хранилище загруженных файлов
```

---

## 🛠️ Технологии

| Категория | Технология |
|-----------|------------|
| **Backend** | Flask (Python веб-фреймворк) |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Desktop GUI** | Tkinter (встроен в Python) |
| **QR-коды** | python-qrcode + Pillow |
| **Упаковка** | PyInstaller |
| **i18n** | Кастомная система переводов |

---

## 🔐 Примечания по Безопасности

⚠️ **Важная информация о безопасности:**

- ✅ **Безопасно**: Используйте в доверенных локальных сетях (дом, офис)
- ❌ **Небезопасно**: НЕ выставляйте в интернет без защиты
- 🔒 **Функции**: Ограничение размера файлов, валидация путей
- 🏠 **Рекомендуется**: Только локальная сеть

**Это для локального обмена файлами, не production веб-сервер!**

---

## 💡 Сценарии Использования

### 1. Передача Фото (Телефон → ПК)
- Запустите сервер на ПК
- Отсканируйте QR телефоном
- Загрузите фото мгновенно
- ✅ Готово за секунды!

### 2. Обмен Файлами (Офис/Дом)
- Один человек запускает сервер
- Все подключаются по IP
- Свободная загрузка/скачивание
- ✅ Не нужны email вложения!

### 3. Резервное Копирование Папок
- Перетащите папку в браузер
- Полная структура загружена
- Скачайте как ZIP в любое время
- ✅ Легкие бэкапы!

---

## 🎨 Превью Интерфейса

### Возможности Веб-Интерфейса:
- 🌙 **Темная тема** с фиолетовыми градиентами
- 🎯 **Drag & Drop** зона загрузки
- 📊 **Индикаторы прогресса** для загрузок
- 🔍 **Поисковая строка** с мгновенной фильтрацией
- 📱 **Адаптивный** дизайн для мобильных
- 🌐 **Переключатель языка** (EN/RU)

### Возможности GUI Launcher:
- 🖥️ **Современный темный интерфейс**
- ▶️ **Запуск/остановка** в один клик
- ⚙️ **Панель настроек** (порт, папка)
- 📡 **Отображение** сетевой информации
- 📱 **Встроенный** QR-код
- 🌐 **Кнопка браузера**

---

## 🆚 Сравнение Версий

| Функция | Простая CMD | Полная GUI |
|---------|:-----------:|:----------:|
| Красивый Веб UI | ✅ | ✅ |
| Drag & Drop | ❌ | ✅ |
| Загрузка Папок | ❌ | ✅ |
| Поиск и Сортировка | ❌ | ✅ |
| Удаление Файлов | ❌ | ✅ |
| Прогресс-бар | ❌ | ✅ |
| QR-код | ❌ | ✅ |
| GUI Launcher | ❌ | ✅ |
| Мультиязычность | ❌ | ✅ |
| Размер Файла | ~5 МБ | ~15 МБ |

**Рекомендация**: Используйте **GUI версию** для лучшего опыта!

---

## 📋 Требования

### Минимальные:
- **ОС**: Windows 7+, Linux, macOS
- **Python**: 3.7 или выше
- **RAM**: 100 МБ
- **Диск**: 50 МБ

### Зависимости (устанавливаются автоматически):
```
Flask==3.0.0
qrcode==7.4.2
Pillow==10.1.0
pyinstaller==6.3.0  # Только для сборки .exe
```

---

## 🤝 Вклад в Проект

Вклад приветствуется! Вы можете:
- 🐛 Сообщать об ошибках
- 💡 Предлагать функции
- 🌍 Добавлять переводы
- 📝 Улучшать документацию
- 🔧 Отправлять pull requests

---

## 📄 Лицензия

**MIT License** - Свободно используйте для любых целей!

См. файл [LICENSE](LICENSE) для деталей.

---

## 🎉 История Изменений

### Версия 2.0 (Текущая)
- ✨ Полный редизайн UI
- 🌍 Поддержка нескольких языков (EN/RU)
- 📤 Drag & Drop загрузка
- 📁 Поддержка папок с ZIP
- 🖥️ Профессиональный GUI launcher
- 📱 Генерация QR-кода
- 🔍 Функции поиска и сортировки
- 📦 Несколько вариантов .exe

### Версия 1.0 (Устаревшая)
- Базовая загрузка/скачивание файлов
- Простой интерфейс списком
- Доступ в локальной сети

---

## 📞 Поддержка

Возникли проблемы? Проверьте:
1. [Документацию](#документация)
2. [Частые Проблемы](#частые-проблемы)
3. Откройте issue на GitHub

---

## 🙏 Благодарности

Создано с ❤️ используя:
- **Flask** - Веб-фреймворк
- **Python** - Язык программирования
- **Tkinter** - GUI фреймворк
- Сообщество открытого ПО

---

<div align="center">

**⭐ Поставьте звезду этому репозиторию если он полезен!**

Сделано с ❤️ | [Сообщить об Ошибке](../../issues) | [Запросить Функцию](../../issues)

</div>
