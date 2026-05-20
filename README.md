# ⚡ QuickShare

A fast, zero-config file transfer server for your local network. Run one
executable, open the link on your phone or another computer, and move files
both ways — no cloud, no accounts, no setup.

QuickShare is a single self-contained binary written in Go. There is nothing
to install: the web interface, QR generator and all assets are embedded in the
`.exe`.

## Features

- **Single executable** — no runtime, no dependencies, no installer.
- **Drag & drop** uploads of files *and* whole folders.
- **Download** files directly, or whole folders as a streamed ZIP.
- **QR code** for instant access from a phone.
- **Modern UI** — responsive, light/dark theme, English & Russian.
- **Live sync** — the listing refreshes automatically across devices.
- **Safe** — path-traversal protection on every file operation.

## Usage

Download `quickshare.exe` (or build it — see below) and run it:

```
quickshare.exe
```

The console prints the network address and opens your browser. Open the same
address on any other device on the network, or scan the in-page QR code.

### Options

| Flag           | Default     | Description                              |
|----------------|-------------|------------------------------------------|
| `-port`        | `8000`      | Port to listen on                        |
| `-dir`         | `uploads`   | Folder where shared files are stored     |
| `-no-browser`  | `false`     | Do not open the browser on start         |

```
quickshare.exe -port 9000 -dir D:\Shared
```

## Build from source

Requires [Go](https://go.dev/dl/) 1.26 or newer.

```
go mod tidy
go build -ldflags "-s -w" -o quickshare.exe
```

The resulting `quickshare.exe` is fully standalone.

## License

MIT — see [LICENSE](LICENSE).
