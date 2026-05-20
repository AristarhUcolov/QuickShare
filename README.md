<div align="center">

# ⚡ QuickShare

**Send files between your devices over the local network.**
One executable. Nothing to install.

<a href="#eng">English</a> &nbsp;•&nbsp; <a href="#ru">Русский</a>

</div>

---

<a id="eng"></a>

## English

QuickShare turns any Windows PC into a quick file drop for your network.
Start it, and every phone, laptop or tablet on the same Wi-Fi can open a web
page to send files in and pick files up. No cloud, no accounts, and nothing to
install on the other device — it only needs a browser.

The whole thing is a single Go executable. The interface, assets and QR
generator live inside the `.exe`, so there is no runtime to set up and no
folder of dependencies to carry around.

### Running it

Grab `quickshare.exe` and double-click it (or run it from a terminal). A
console window shows the address and your browser opens automatically:

```
quickshare.exe
```

On any other device, open the address shown as **Network**, or scan the QR
code from the button in the top-right corner of the page.

### Options

| Flag          | Default   | What it does                          |
|---------------|-----------|---------------------------------------|
| `-port`       | `8000`    | Port to listen on                     |
| `-dir`        | `uploads` | Folder where shared files are kept    |
| `-no-browser` | off       | Don't open the browser on start       |

```
quickshare.exe -port 9000 -dir D:\Shared
```

### What it can do

- Drag and drop files, or whole folders, straight onto the page.
- Download single files, or grab a whole folder as a ZIP (built on the fly,
  never written to disk).
- A QR code so a phone can join without typing anything.
- Light and dark themes, English and Russian, a search box and sorting.
- The file list refreshes by itself, so every device stays in sync.

### Building from source

You'll need [Go](https://go.dev/dl/) 1.26 or newer.

```
go mod tidy
go build -ldflags "-s -w" -o quickshare.exe
```

The `quickshare.exe` you get is completely standalone — copy it anywhere and
it just runs.

### A note on safety

QuickShare has no password and is meant for networks you trust (home or
office Wi-Fi). Anyone who can reach the address can upload, download and
delete files. Every path is checked so requests can't escape the shared
folder, but don't expose the port to the open internet.

<div align="right"><a href="#ru">→ Русская версия</a></div>

---

<a id="ru"></a>

## Русский

QuickShare превращает любой компьютер на Windows в быстрый обменник файлов
для вашей сети. Запустите его — и любой телефон, ноутбук или планшет в той же
Wi-Fi сети сможет открыть веб-страницу, чтобы отправить или забрать файлы.
Без облака, без регистрации и без установки чего-либо на другом устройстве —
ему нужен только браузер.

Вся программа — это один исполняемый файл на Go. Интерфейс, ресурсы и
генератор QR-кода находятся внутри `.exe`, поэтому ничего настраивать и
таскать с собой папку с зависимостями не нужно.

### Запуск

Возьмите `quickshare.exe` и запустите двойным щелчком (или из терминала).
В консоли появится адрес, а браузер откроется сам:

```
quickshare.exe
```

На другом устройстве откройте адрес из строки **Network** или отсканируйте
QR-код — кнопка в правом верхнем углу страницы.

### Параметры

| Флаг          | По умолчанию | Назначение                            |
|---------------|--------------|---------------------------------------|
| `-port`       | `8000`       | Порт, который слушает сервер          |
| `-dir`        | `uploads`    | Папка, где хранятся общие файлы       |
| `-no-browser` | выкл.        | Не открывать браузер при запуске      |

```
quickshare.exe -port 9000 -dir D:\Shared
```

### Что умеет

- Перетаскивание файлов и целых папок прямо на страницу.
- Скачивание отдельных файлов или папки целиком в виде ZIP — архив
  собирается на лету и не пишется на диск.
- QR-код, чтобы телефон подключился без ввода адреса вручную.
- Светлая и тёмная темы, русский и английский, поиск и сортировка.
- Список файлов обновляется сам, поэтому все устройства видят одно и то же.

### Сборка из исходников

Понадобится [Go](https://go.dev/dl/) версии 1.26 или новее.

```
go mod tidy
go build -ldflags "-s -w" -o quickshare.exe
```

Полученный `quickshare.exe` полностью самостоятельный — скопируйте его куда
угодно, и он просто запустится.

### О безопасности

В QuickShare нет пароля, он рассчитан на сети, которым вы доверяете (домашняя
или офисная Wi-Fi). Любой, кто откроет адрес, сможет загружать, скачивать и
удалять файлы. Все пути проверяются, чтобы запросы не выходили за пределы
общей папки, но не открывайте порт в интернет.

<div align="right"><a href="#eng">→ English version</a></div>

---

<div align="center">
MIT License &nbsp;•&nbsp; see <a href="LICENSE">LICENSE</a>
</div>
