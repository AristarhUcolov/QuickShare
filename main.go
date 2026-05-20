// QuickShare — a fast, zero-config file transfer server for your local network.
package main

import (
	"flag"
	"fmt"
	"net"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
)

const version = "3.0"

func main() {
	port := flag.Int("port", 8000, "port to listen on")
	dir := flag.String("dir", "uploads", "directory where shared files are stored")
	noBrowser := flag.Bool("no-browser", false, "do not open the browser on start")
	flag.Parse()

	absDir, err := filepath.Abs(*dir)
	if err != nil {
		fatal("invalid directory: " + err.Error())
	}
	if err := os.MkdirAll(absDir, 0o755); err != nil {
		fatal("cannot create directory: " + err.Error())
	}

	srv := NewServer(absDir, *port)
	ip := localIP()
	url := fmt.Sprintf("http://%s:%d", ip, *port)

	banner(url, *port, absDir)

	if !*noBrowser {
		openBrowser(fmt.Sprintf("http://localhost:%d", *port))
	}

	if err := srv.Run(); err != nil {
		fatal("server stopped: " + err.Error())
	}
}

// localIP returns the machine's primary LAN address, or 127.0.0.1 if offline.
func localIP() string {
	conn, err := net.Dial("udp", "8.8.8.8:80")
	if err != nil {
		return "127.0.0.1"
	}
	defer conn.Close()
	return conn.LocalAddr().(*net.UDPAddr).IP.String()
}

// openBrowser launches the default browser pointing at url, best-effort.
func openBrowser(url string) {
	var cmd string
	var args []string
	switch runtime.GOOS {
	case "windows":
		cmd, args = "rundll32", []string{"url.dll,FileProtocolHandler", url}
	case "darwin":
		cmd, args = "open", []string{url}
	default:
		cmd, args = "xdg-open", []string{url}
	}
	_ = exec.Command(cmd, args...).Start()
}

func banner(url string, port int, dir string) {
	line := strings.Repeat("─", 52)
	fmt.Printf("\n┌%s┐\n", line)
	fmt.Printf("│  QuickShare %-39s│\n", "v"+version)
	fmt.Printf("│  Local network file transfer%-23s│\n", "")
	fmt.Printf("├%s┤\n", line)
	fmt.Printf("│  Network   %-41s│\n", url)
	fmt.Printf("│  Local     %-41s│\n", fmt.Sprintf("http://localhost:%d", port))
	fmt.Printf("│  Folder    %-41s│\n", truncate(dir, 41))
	fmt.Printf("├%s┤\n", line)
	fmt.Printf("│  Open the network address on any device, or scan  │\n")
	fmt.Printf("│  the QR code in the web page. Press Ctrl+C to stop.│\n")
	fmt.Printf("└%s┘\n\n", line)
}

func truncate(s string, n int) string {
	if len(s) <= n {
		return s
	}
	return "…" + s[len(s)-n+1:]
}

func fatal(msg string) {
	fmt.Fprintln(os.Stderr, "error: "+msg)
	os.Exit(1)
}
