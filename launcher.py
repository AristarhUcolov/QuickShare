import tkinter as tk
from tkinter import ttk, messagebox
import threading
import subprocess
import socket
import webbrowser
import sys
import os
from pathlib import Path
import qrcode
from PIL import Image, ImageTk
from io import BytesIO

class ServerLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("🚀 QuickShare - LAN File Transfer")
        self.root.geometry("650x800")
        self.root.resizable(True, True)
        
        # Переменные
        self.server_process = None
        self.is_running = False
        self.port = tk.StringVar(value="8000")
        self.upload_folder = tk.StringVar(value="uploads")
        
        # Получить IP
        self.local_ip = self.get_local_ip()
        
        # Настроить стиль
        self.setup_style()
        
        # Создать интерфейс
        self.create_widgets()
        
    def setup_style(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цвета
        bg_color = "#0f172a"
        fg_color = "#f1f5f9"
        primary = "#6366f1"
        success = "#10b981"
        danger = "#ef4444"
        
        self.root.configure(bg=bg_color)
        
        # Стили для кнопок
        style.configure("Primary.TButton",
                       background=primary,
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none",
                       font=('Segoe UI', 11, 'bold'),
                       padding=15)
        
        style.map("Primary.TButton",
                 background=[('active', '#4f46e5')])
        
        style.configure("Success.TButton",
                       background=success,
                       foreground="white",
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'),
                       padding=15)
        
        style.map("Success.TButton",
                 background=[('active', '#059669')])
        
        style.configure("Danger.TButton",
                       background=danger,
                       foreground="white",
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'),
                       padding=15)
        
        style.map("Danger.TButton",
                 background=[('active', '#dc2626')])
        
        # Стили для Entry
        style.configure("Custom.TEntry",
                       fieldbackground="#1e293b",
                       foreground=fg_color,
                       borderwidth=2,
                       relief="solid")
        
        # Стили для Label
        style.configure("Title.TLabel",
                       background=bg_color,
                       foreground=fg_color,
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure("Subtitle.TLabel",
                       background=bg_color,
                       foreground="#94a3b8",
                       font=('Segoe UI', 11))
        
        style.configure("Status.TLabel",
                       background=bg_color,
                       foreground=fg_color,
                       font=('Segoe UI', 12, 'bold'))
        
        style.configure("Info.TLabel",
                       background="#1e293b",
                       foreground=fg_color,
                       font=('Segoe UI', 10),
                       padding=10)
        
    def create_widgets(self):
        # Создать canvas со scrollbar
        canvas = tk.Canvas(self.root, bg="#0f172a", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#0f172a")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Упаковать canvas и scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Прокрутка мышью
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main_frame = tk.Frame(scrollable_frame, bg="#0f172a")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="🚀 QuickShare", style="Title.TLabel")
        title_label.pack(pady=(0, 5))
        
        subtitle_label = ttk.Label(main_frame, text="Локальный сервер для обмена файлами", style="Subtitle.TLabel")
        subtitle_label.pack(pady=(0, 20))
        
        # Статус сервера
        status_frame = tk.Frame(main_frame, bg="#1e293b", relief=tk.FLAT, bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 20), ipady=15)
        
        tk.Label(status_frame, text="Статус:", bg="#1e293b", fg="#94a3b8", font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        
        self.status_label = tk.Label(status_frame, text="⭕ Остановлен", bg="#1e293b", fg="#ef4444", font=('Segoe UI', 12, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Настройки
        settings_frame = tk.LabelFrame(main_frame, text="  ⚙️ Настройки  ", bg="#1e293b", fg="#f1f5f9", 
                                      font=('Segoe UI', 11, 'bold'), bd=2, relief=tk.GROOVE)
        settings_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Порт
        port_frame = tk.Frame(settings_frame, bg="#1e293b")
        port_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(port_frame, text="Порт:", bg="#1e293b", fg="#f1f5f9", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        port_entry = tk.Entry(port_frame, textvariable=self.port, bg="#334155", fg="#f1f5f9", 
                             font=('Segoe UI', 10), width=10, relief=tk.FLAT, bd=5)
        port_entry.pack(side=tk.LEFT, padx=10)
        
        # Папка загрузок
        folder_frame = tk.Frame(settings_frame, bg="#1e293b")
        folder_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        tk.Label(folder_frame, text="Папка:", bg="#1e293b", fg="#f1f5f9", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        folder_entry = tk.Entry(folder_frame, textvariable=self.upload_folder, bg="#334155", fg="#f1f5f9",
                               font=('Segoe UI', 10), width=30, relief=tk.FLAT, bd=5)
        folder_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Информация о подключении
        info_frame = tk.LabelFrame(main_frame, text="  📡 Информация о подключении  ", bg="#1e293b", fg="#f1f5f9",
                                  font=('Segoe UI', 11, 'bold'), bd=2, relief=tk.GROOVE)
        info_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.ip_label = tk.Label(info_frame, text=f"Локальный IP: {self.local_ip}", 
                                bg="#1e293b", fg="#10b981", font=('Segoe UI', 11), anchor=tk.W)
        self.ip_label.pack(fill=tk.X, padx=15, pady=10)
        
        self.url_label = tk.Label(info_frame, text="URL: Не запущен", 
                                 bg="#1e293b", fg="#94a3b8", font=('Segoe UI', 11), anchor=tk.W)
        self.url_label.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        # QR код
        self.qr_frame = tk.LabelFrame(main_frame, text="  📱 QR-код для быстрого доступа  ", bg="#1e293b", fg="#f1f5f9",
                                     font=('Segoe UI', 11, 'bold'), bd=2, relief=tk.GROOVE)
        self.qr_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.qr_label = tk.Label(self.qr_frame, text="QR-код будет доступен после запуска сервера", 
                                bg="#1e293b", fg="#94a3b8", font=('Segoe UI', 9))
        self.qr_label.pack(pady=15)
        
        # Кнопки управления
        buttons_frame = tk.Frame(main_frame, bg="#0f172a")
        buttons_frame.pack(fill=tk.X)
        
        self.start_btn = tk.Button(buttons_frame, text="▶️  Запустить сервер", 
                                   command=self.start_server,
                                   bg="#10b981", fg="white", font=('Segoe UI', 12, 'bold'),
                                   relief=tk.FLAT, cursor="hand2", padx=20, pady=15)
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_btn = tk.Button(buttons_frame, text="⏹  Остановить", 
                                 command=self.stop_server,
                                 bg="#ef4444", fg="white", font=('Segoe UI', 12, 'bold'),
                                 relief=tk.FLAT, cursor="hand2", padx=20, pady=15,
                                 state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.browser_btn = tk.Button(buttons_frame, text="🌐  Открыть", 
                                    command=self.open_browser,
                                    bg="#6366f1", fg="white", font=('Segoe UI', 12, 'bold'),
                                    relief=tk.FLAT, cursor="hand2", padx=20, pady=15,
                                    state=tk.DISABLED)
        self.browser_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
    def get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "127.0.0.1"
    
    def generate_qr_code(self, url):
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Конвертировать в PhotoImage
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        pil_image = Image.open(buffer)
        pil_image = pil_image.resize((180, 180), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(pil_image)
        
        self.qr_label.configure(image=photo, text="")
        self.qr_label.image = photo
    
    def start_server(self):
        if self.is_running:
            return
        
        try:
            port = int(self.port.get())
            
            # Создать папку если не существует
            os.makedirs(self.upload_folder.get(), exist_ok=True)
            
            # Запустить сервер в отдельном процессе
            server_script = Path(__file__).parent / "server.py"
            
            if not server_script.exists():
                messagebox.showerror("Ошибка", "Файл server.py не найден!")
                return
            
            # Запустить сервер
            self.server_process = subprocess.Popen(
                [sys.executable, str(server_script)],
                cwd=Path(__file__).parent
            )
            
            self.is_running = True
            
            # Обновить UI
            self.status_label.configure(text="🟢 Запущен", fg="#10b981")
            url = f"http://{self.local_ip}:{port}"
            self.url_label.configure(text=f"URL: {url}", fg="#10b981")
            
            self.start_btn.configure(state=tk.DISABLED)
            self.stop_btn.configure(state=tk.NORMAL)
            self.browser_btn.configure(state=tk.NORMAL)
            
            # Генерировать QR код
            self.generate_qr_code(url)
            
            messagebox.showinfo("Успех", f"Сервер запущен на {url}")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный номер порта!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить сервер:\n{str(e)}")
    
    def stop_server(self):
        if not self.is_running:
            return
        
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
        
        self.is_running = False
        
        # Обновить UI
        self.status_label.configure(text="⭕ Остановлен", fg="#ef4444")
        self.url_label.configure(text="URL: Не запущен", fg="#94a3b8")
        
        self.start_btn.configure(state=tk.NORMAL)
        self.stop_btn.configure(state=tk.DISABLED)
        self.browser_btn.configure(state=tk.DISABLED)
        
        # Очистить QR код
        self.qr_label.configure(image="", text="QR-код будет доступен после запуска сервера")
        
        messagebox.showinfo("Остановлен", "Сервер остановлен")
    
    def open_browser(self):
        if self.is_running:
            url = f"http://{self.local_ip}:{self.port.get()}"
            webbrowser.open(url)
    
    def on_closing(self):
        if self.is_running:
            if messagebox.askokcancel("Выход", "Сервер запущен. Остановить и выйти?"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
