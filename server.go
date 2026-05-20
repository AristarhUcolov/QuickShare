package main

import (
	"archive/zip"
	"embed"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"net/http"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"time"

	qrcode "github.com/skip2/go-qrcode"
)

//go:embed web
var webFS embed.FS

// Server holds the running configuration and serves the QuickShare app.
type Server struct {
	dir  string // absolute path of the shared folder
	port int
}

// NewServer builds a Server for the given shared directory and port.
func NewServer(dir string, port int) *Server {
	return &Server{dir: dir, port: port}
}

// fileEntry is one item in the shared folder, as sent to the browser.
type fileEntry struct {
	Name     string `json:"name"`
	Size     int64  `json:"size"`
	Modified int64  `json:"modified"` // unix seconds
	IsDir    bool   `json:"isDir"`
}

// Run starts the HTTP server and blocks until it stops.
func (s *Server) Run() error {
	static, err := fs.Sub(webFS, "web")
	if err != nil {
		return err
	}

	mux := http.NewServeMux()
	mux.HandleFunc("/", s.handleIndex(static))
	mux.Handle("/assets/", http.StripPrefix("/assets/", http.FileServer(http.FS(mustSub(static, "assets")))))
	mux.HandleFunc("/api/files", s.handleFiles)
	mux.HandleFunc("/api/upload", s.handleUpload)
	mux.HandleFunc("/api/download", s.handleDownload)
	mux.HandleFunc("/api/zip", s.handleZip)
	mux.HandleFunc("/api/delete", s.handleDelete)
	mux.HandleFunc("/api/qr", s.handleQR)

	srv := &http.Server{
		Addr:         fmt.Sprintf(":%d", s.port),
		Handler:      logRequests(mux),
		ReadTimeout:  0, // uploads of large files must not time out
		WriteTimeout: 0,
	}
	return srv.ListenAndServe()
}

func mustSub(f fs.FS, dir string) fs.FS {
	sub, err := fs.Sub(f, dir)
	if err != nil {
		panic(err)
	}
	return sub
}

// logRequests prints a compact one-line log for every request.
func logRequests(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		start := time.Now()
		next.ServeHTTP(w, r)
		fmt.Printf("  %s  %-7s %s  (%s)\n",
			start.Format("15:04:05"), r.Method, r.URL.Path, time.Since(start).Round(time.Millisecond))
	})
}

// handleIndex serves the single-page app for "/" and 404s anything else.
func (s *Server) handleIndex(static fs.FS) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		page, err := fs.ReadFile(static, "index.html")
		if err != nil {
			http.Error(w, "index missing", http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "text/html; charset=utf-8")
		_, _ = w.Write(page)
	}
}

// handleFiles returns the folder listing and aggregate stats as JSON.
func (s *Server) handleFiles(w http.ResponseWriter, r *http.Request) {
	entries, err := os.ReadDir(s.dir)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}

	files := make([]fileEntry, 0, len(entries))
	var total int64
	for _, e := range entries {
		if strings.HasPrefix(e.Name(), ".") {
			continue // hide dotfiles such as .gitkeep
		}
		info, err := e.Info()
		if err != nil {
			continue
		}
		size := info.Size()
		if e.IsDir() {
			size = dirSize(filepath.Join(s.dir, e.Name()))
		}
		total += size
		files = append(files, fileEntry{
			Name:     e.Name(),
			Size:     size,
			Modified: info.ModTime().Unix(),
			IsDir:    e.IsDir(),
		})
	}
	sort.Slice(files, func(i, j int) bool {
		if files[i].IsDir != files[j].IsDir {
			return files[i].IsDir // folders first
		}
		return strings.ToLower(files[i].Name) < strings.ToLower(files[j].Name)
	})

	writeJSON(w, http.StatusOK, map[string]any{
		"files":     files,
		"count":     len(files),
		"totalSize": total,
	})
}

// handleUpload accepts a streamed multipart upload of one or more files.
func (s *Server) handleUpload(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	reader, err := r.MultipartReader()
	if err != nil {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "bad upload"})
		return
	}

	saved := 0
	for {
		part, err := reader.NextPart()
		if errors.Is(err, io.EOF) {
			break
		}
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]string{"error": err.Error()})
			return
		}
		if part.FormName() != "files" || part.FileName() == "" {
			continue
		}
		dest, err := safeJoin(s.dir, part.FileName())
		if err != nil {
			continue // reject path-traversal attempts silently
		}
		if err := os.MkdirAll(filepath.Dir(dest), 0o755); err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		f, err := os.Create(dest)
		if err != nil {
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		if _, err := io.Copy(f, part); err != nil {
			f.Close()
			writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
			return
		}
		f.Close()
		saved++
	}
	writeJSON(w, http.StatusOK, map[string]any{"status": "ok", "count": saved})
}

// handleDownload streams a single file as an attachment.
func (s *Server) handleDownload(w http.ResponseWriter, r *http.Request) {
	target, err := safeJoin(s.dir, r.URL.Query().Get("path"))
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	info, err := os.Stat(target)
	if err != nil || info.IsDir() {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	w.Header().Set("Content-Disposition", attachment(info.Name()))
	http.ServeFile(w, r, target)
}

// handleZip streams a folder as a ZIP archive without touching disk.
func (s *Server) handleZip(w http.ResponseWriter, r *http.Request) {
	target, err := safeJoin(s.dir, r.URL.Query().Get("path"))
	if err != nil {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}
	info, err := os.Stat(target)
	if err != nil || !info.IsDir() {
		http.Error(w, "not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/zip")
	w.Header().Set("Content-Disposition", attachment(info.Name()+".zip"))

	zw := zip.NewWriter(w)
	defer zw.Close()
	_ = filepath.WalkDir(target, func(path string, d fs.DirEntry, err error) error {
		if err != nil || d.IsDir() {
			return err
		}
		rel, err := filepath.Rel(target, path)
		if err != nil {
			return err
		}
		entry, err := zw.Create(filepath.ToSlash(rel))
		if err != nil {
			return err
		}
		src, err := os.Open(path)
		if err != nil {
			return err
		}
		defer src.Close()
		_, err = io.Copy(entry, src)
		return err
	})
}

// handleDelete removes a file or folder from the shared directory.
func (s *Server) handleDelete(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodDelete {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}
	target, err := safeJoin(s.dir, r.URL.Query().Get("path"))
	if err != nil {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "not found"})
		return
	}
	if err := os.RemoveAll(target); err != nil {
		writeJSON(w, http.StatusInternalServerError, map[string]string{"error": err.Error()})
		return
	}
	writeJSON(w, http.StatusOK, map[string]string{"status": "ok"})
}

// handleQR returns a PNG QR code that encodes the LAN address of the server.
func (s *Server) handleQR(w http.ResponseWriter, r *http.Request) {
	url := fmt.Sprintf("http://%s:%d", localIP(), s.port)
	png, err := qrcode.Encode(url, qrcode.Medium, 320)
	if err != nil {
		http.Error(w, "qr error", http.StatusInternalServerError)
		return
	}
	w.Header().Set("Content-Type", "image/png")
	w.Header().Set("Cache-Control", "no-store")
	_, _ = w.Write(png)
}

// safeJoin joins name onto base and guarantees the result stays inside base,
// blocking "../" path-traversal attacks.
func safeJoin(base, name string) (string, error) {
	if name == "" {
		return "", errors.New("empty path")
	}
	clean := filepath.Clean("/" + strings.ReplaceAll(name, "\\", "/"))
	joined := filepath.Join(base, clean)
	if joined != base && !strings.HasPrefix(joined, base+string(os.PathSeparator)) {
		return "", errors.New("path escapes base")
	}
	return joined, nil
}

// dirSize returns the total size of all files under path.
func dirSize(path string) int64 {
	var total int64
	_ = filepath.WalkDir(path, func(_ string, d fs.DirEntry, err error) error {
		if err == nil && !d.IsDir() {
			if info, err := d.Info(); err == nil {
				total += info.Size()
			}
		}
		return nil
	})
	return total
}

// attachment builds a Content-Disposition header that survives non-ASCII names.
func attachment(name string) string {
	return fmt.Sprintf(`attachment; filename*=UTF-8''%s`, urlEscape(name))
}

func urlEscape(s string) string {
	const hex = "0123456789ABCDEF"
	var b strings.Builder
	for _, c := range []byte(s) {
		if (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') ||
			(c >= '0' && c <= '9') || strings.IndexByte("-_.~", c) >= 0 {
			b.WriteByte(c)
		} else {
			b.WriteByte('%')
			b.WriteByte(hex[c>>4])
			b.WriteByte(hex[c&0x0f])
		}
	}
	return b.String()
}

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}
