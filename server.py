from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for, jsonify, send_file, make_response
import os
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
import socket
import qrcode
from io import BytesIO
import base64
from translations import get_translation

# Использовать переменную окружения если установлена, иначе "uploads"
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max

def get_local_ip():
    """Get local IP address / Получить локальный IP адрес"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_current_language():
    """Get current language from cookie or query parameter"""
    lang = request.args.get('lang', request.cookies.get('language', 'en'))
    return lang if lang in ['en', 'ru'] else 'en'

def format_size(size, lang='en'):
    """Format file size / Форматировать размер файла"""
    t = get_translation(lang)
    units = [t['size_b'], t['size_kb'], t['size_mb'], t['size_gb']]
    for unit in units:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} {t['size_tb']}"

def get_file_info(path, lang='en'):
    """Get file/folder information / Получить информацию о файле/папке"""
    stat = os.stat(path)
    is_dir = os.path.isdir(path)
    
    if is_dir:
        size = sum(f.stat().st_size for f in Path(path).rglob('*') if f.is_file())
    else:
        size = stat.st_size
    
    return {
        'name': os.path.basename(path),
        'size': size,
        'size_formatted': format_size(size, lang),
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'is_dir': is_dir
    }

def create_zip_from_folder(folder_path, zip_path):
    """Create ZIP archive from folder / Создать ZIP архив из папки"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🚀 LAN File Share Pro</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #6366f1;
    --primary-dark: #4f46e5;
    --danger: #ef4444;
    --success: #10b981;
    --bg: #0f172a;
    --bg-light: #1e293b;
    --bg-card: #334155;
    --text: #f1f5f9;
    --text-muted: #94a3b8;
    --border: #475569;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
    color: var(--text);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.9), rgba(139, 92, 246, 0.9));
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    margin-bottom: 30px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 20px;
}

.header h1 {
    font-size: 2.5em;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 15px;
}

.stats {
    display: flex;
    gap: 30px;
    font-size: 0.95em;
}

.stat-item {
    text-align: center;
}

.stat-value {
    font-size: 1.5em;
    font-weight: 700;
    color: #fbbf24;
}

.stat-label {
    opacity: 0.9;
    margin-top: 5px;
}

.upload-zone {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(10px);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 30px;
    border: 3px dashed var(--border);
    transition: all 0.3s ease;
    cursor: pointer;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.upload-zone.dragover {
    border-color: var(--primary);
    background: rgba(99, 102, 241, 0.2);
    transform: scale(1.02);
}

.upload-content {
    text-align: center;
}

.upload-icon {
    font-size: 4em;
    margin-bottom: 20px;
    opacity: 0.8;
}

.upload-zone h3 {
    font-size: 1.5em;
    margin-bottom: 10px;
}

.upload-zone p {
    color: var(--text-muted);
    margin-bottom: 20px;
}

.upload-buttons {
    display: flex;
    gap: 15px;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    padding: 12px 30px;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 1em;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    text-decoration: none;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
}

.btn-success {
    background: linear-gradient(135deg, var(--success), #059669);
    color: white;
}

.btn-danger {
    background: linear-gradient(135deg, var(--danger), #dc2626);
    color: white;
}

.btn-secondary {
    background: rgba(148, 163, 184, 0.2);
    color: var(--text);
}

.search-sort {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.search-box {
    flex: 1;
    min-width: 250px;
    position: relative;
}

.search-box input {
    width: 100%;
    padding: 12px 15px 12px 45px;
    border: 2px solid var(--border);
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.6);
    color: var(--text);
    font-size: 1em;
    transition: all 0.3s ease;
}

.search-box input:focus {
    outline: none;
    border-color: var(--primary);
    background: rgba(15, 23, 42, 0.9);
}

.search-icon {
    position: absolute;
    left: 15px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 1.2em;
    opacity: 0.5;
}

.sort-buttons {
    display: flex;
    gap: 10px;
}

.files-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.file-card {
    background: rgba(30, 41, 59, 0.9);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    transition: all 0.3s ease;
    border: 2px solid transparent;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.file-card:hover {
    transform: translateY(-5px);
    border-color: var(--primary);
    box-shadow: 0 15px 40px rgba(99, 102, 241, 0.3);
}

.file-icon {
    font-size: 3em;
    margin-bottom: 15px;
    display: block;
}

.file-name {
    font-size: 1.1em;
    font-weight: 600;
    margin-bottom: 10px;
    word-break: break-word;
}

.file-meta {
    display: flex;
    justify-content: space-between;
    color: var(--text-muted);
    font-size: 0.9em;
    margin-bottom: 15px;
}

.file-actions {
    display: flex;
    gap: 10px;
}

.file-actions .btn {
    flex: 1;
    padding: 8px 15px;
    font-size: 0.9em;
    justify-content: center;
}

.progress-container {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 350px;
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    display: none;
    z-index: 1000;
}

.progress-container.show {
    display: block;
    animation: slideIn 0.3s ease;
}

@keyframes slideIn {
    from {
        transform: translateX(400px);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
    font-weight: 600;
}

.progress-bar {
    height: 8px;
    background: rgba(71, 85, 105, 0.5);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 10px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--primary), var(--success));
    transition: width 0.3s ease;
    border-radius: 10px;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    background: rgba(30, 41, 59, 0.6);
    border-radius: 15px;
}

.empty-state-icon {
    font-size: 5em;
    opacity: 0.3;
    margin-bottom: 20px;
}

.qr-modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    z-index: 2000;
    align-items: center;
    justify-content: center;
}

.qr-modal.show {
    display: flex;
}

.qr-content {
    background: rgba(30, 41, 59, 0.95);
    backdrop-filter: blur(10px);
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    max-width: 400px;
}

.qr-content img {
    margin: 20px 0;
    border-radius: 10px;
}

input[type="file"] {
    display: none;
}

@media (max-width: 768px) {
    .header h1 {
        font-size: 1.8em;
    }
    
    .stats {
        width: 100%;
        justify-content: space-around;
    }
    
    .files-grid {
        grid-template-columns: 1fr;
    }
    
    .progress-container {
        width: calc(100% - 40px);
        left: 20px;
        right: 20px;
    }
}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>{{ t['title'] }}</h1>
        <div class="stats">
            <div class="stat-item">
                <div class="stat-value" id="fileCount">{{ files|length }}</div>
                <div class="stat-label">{{ t['files_count'] }}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="totalSize">{{ total_size }}</div>
                <div class="stat-label">{{ t['total_size'] }}</div>
            </div>
        </div>
        <div style="display: flex; gap: 10px;">
            <button class="btn btn-secondary" onclick="switchLanguage()">🌐 {{ t['lang_switch'] }}</button>
            <button class="btn btn-secondary" onclick="showQR()">{{ t['qr_button'] }}</button>
        </div>
    </div>

    <div class="upload-zone" id="uploadZone">
        <div class="upload-content">
            <div class="upload-icon">📤</div>
            <h3>{{ t['upload_title'] }}</h3>
            <p>{{ t['upload_desc'] }}</p>
            <div class="upload-buttons">
                <label class="btn btn-primary" onclick="event.stopPropagation()">
                    <input type="file" id="fileInput" multiple onchange="handleFiles(this.files)">
                    {{ t['select_files'] }}
                </label>
                <label class="btn btn-success" onclick="event.stopPropagation()">
                    <input type="file" id="folderInput" webkitdirectory directory multiple onchange="handleFiles(this.files)">
                    {{ t['select_folder'] }}
                </label>
            </div>
        </div>
    </div>

    <div class="search-sort">
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="searchInput" placeholder="{{ t['search_placeholder'] }}" oninput="filterFiles()">
        </div>
        <div class="sort-buttons">
            <button class="btn btn-secondary" onclick="sortFiles('name')">{{ t['sort_name'] }}</button>
            <button class="btn btn-secondary" onclick="sortFiles('size')">{{ t['sort_size'] }}</button>
            <button class="btn btn-secondary" onclick="sortFiles('date')">{{ t['sort_date'] }}</button>
        </div>
    </div>

    <div class="files-grid" id="filesGrid">
        {% if files %}
            {% for file in files %}
            <div class="file-card" data-name="{{ file.name|lower }}" data-size="{{ file.size }}" data-date="{{ file.modified }}">
                <div class="file-icon">{{ '📁' if file.is_dir else '📄' }}</div>
                <div class="file-name">{{ file.name }}</div>
                <div class="file-meta">
                    <span>{{ file.size_formatted }}</span>
                    <span>{{ file.modified }}</span>
                </div>
                <div class="file-actions">
                    {% if file.is_dir %}
                        <a href="/download_folder/{{ file.name }}" class="btn btn-primary">⬇️ ZIP</a>
                    {% else %}
                        <a href="/download/{{ file.name }}" class="btn btn-primary">⬇️</a>
                    {% endif %}
                    <button class="btn btn-danger" onclick="deleteFile('{{ file.name }}')">🗑️</button>
                </div>
            </div>
            {% endfor %}
        {% else %}
            <div class="empty-state">
                <div class="empty-state-icon">📭</div>
                <h3>{{ t['no_files'] }}</h3>
                <p>{{ t['no_files_desc'] }}</p>
            </div>
        {% endif %}
    </div>
</div>

<div class="progress-container" id="progressContainer">
    <div class="progress-header">
        <span id="progressText">{{ t['uploading'] }}</span>
        <span id="progressPercent">0%</span>
    </div>
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>
    <div id="progressDetails"></div>
</div>

<div class="qr-modal" id="qrModal" onclick="hideQR()">
    <div class="qr-content" onclick="event.stopPropagation()">
        <h2>{{ t['scan_qr'] }}</h2>
        <img src="{{ qr_code }}" alt="QR Code" style="max-width: 100%;">
        <p style="margin-top: 15px; word-break: break-all;">{{ server_url }}</p>
        <button class="btn btn-primary" onclick="hideQR()" style="margin-top: 20px;">{{ t['close'] }}</button>
    </div>
</div>

<script>
const uploadZone = document.getElementById('uploadZone');
const progressContainer = document.getElementById('progressContainer');

// Клик по зоне (кроме кнопок)
uploadZone.addEventListener('click', (e) => {
    if (e.target === uploadZone || e.target.closest('.upload-content') && !e.target.closest('.upload-buttons')) {
        document.getElementById('fileInput').click();
    }
});

// Drag & Drop
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    uploadZone.addEventListener(eventName, () => uploadZone.classList.add('dragover'));
});

['dragleave', 'drop'].forEach(eventName => {
    uploadZone.addEventListener(eventName, () => uploadZone.classList.remove('dragover'));
});

uploadZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    handleFiles(files);
});

async function handleFiles(files) {
    if (files.length === 0) return;
    
    progressContainer.classList.add('show');
    const formData = new FormData();
    
    for (let file of files) {
        formData.append('files', file);
    }
    
    try {
        const xhr = new XMLHttpRequest();
        
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = Math.round((e.loaded / e.total) * 100);
                document.getElementById('progressFill').style.width = percent + '%';
                document.getElementById('progressPercent').textContent = percent + '%';
                document.getElementById('progressText').textContent = `Загрузка ${files.length} файлов...`;
            }
        });
        
        xhr.addEventListener('load', () => {
            if (xhr.status === 200) {
                setTimeout(() => {
                    progressContainer.classList.remove('show');
                    location.reload();
                }, 1000);
            }
        });
        
        xhr.open('POST', '/upload');
        xhr.send(formData);
        
    } catch (error) {
        alert('Ошибка загрузки: ' + error);
        progressContainer.classList.remove('show');
    }
}

async function deleteFile(filename) {
    if (!confirm(`Удалить "${filename}"?`)) return;
    
    try {
        const response = await fetch(`/delete/${encodeURIComponent(filename)}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            location.reload();
        } else {
            alert('Ошибка удаления файла');
        }
    } catch (error) {
        alert('Ошибка: ' + error);
    }
}

function filterFiles() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const cards = document.querySelectorAll('.file-card');
    
    cards.forEach(card => {
        const name = card.getAttribute('data-name');
        if (name.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function sortFiles(criteria) {
    const grid = document.getElementById('filesGrid');
    const cards = Array.from(document.querySelectorAll('.file-card'));
    
    cards.sort((a, b) => {
        if (criteria === 'name') {
            return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
        } else if (criteria === 'size') {
            return parseInt(b.getAttribute('data-size')) - parseInt(a.getAttribute('data-size'));
        } else if (criteria === 'date') {
            return b.getAttribute('data-date').localeCompare(a.getAttribute('data-date'));
        }
    });
    
    cards.forEach(card => grid.appendChild(card));
}

function showQR() {
    document.getElementById('qrModal').classList.add('show');
}

function hideQR() {
    document.getElementById('qrModal').classList.remove('show');
}

function switchLanguage() {
    const currentLang = '{{ lang }}';
    const newLang = currentLang === 'en' ? 'ru' : 'en';
    window.location.href = '?lang=' + newLang;
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    lang = get_current_language()
    t = get_translation(lang)
    files_info = []
    total_size = 0
    
    for item in os.listdir(UPLOAD_FOLDER):
        item_path = os.path.join(UPLOAD_FOLDER, item)
        info = get_file_info(item_path, lang)
        files_info.append(info)
        total_size += info['size']
    
    # Generate QR code / Генерация QR кода
    local_ip = get_local_ip()
    server_url = f"http://{local_ip}:8000"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(server_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    qr_data_uri = f"data:image/png;base64,{qr_base64}"
    
    response = make_response(render_template_string(
        HTML, 
        files=sorted(files_info, key=lambda x: x['name']),
        total_size=format_size(total_size, lang),
        qr_code=qr_data_uri,
        server_url=server_url,
        t=t,
        lang=lang
    ))
    
    # Set language cookie if specified in URL
    if 'lang' in request.args:
        response.set_cookie('language', lang, max_age=30*24*60*60)
    
    return response

@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")
    
    for file in files:
        if file and file.filename:
            # Сохранить структуру папок
            filename = file.filename
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            # Создать директории если нужно
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
    
    return jsonify({"status": "success", "count": len(files)})

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/download_folder/<path:foldername>")
def download_folder(foldername):
    folder_path = os.path.join(UPLOAD_FOLDER, foldername)
    
    if not os.path.isdir(folder_path):
        return "Папка не найдена", 404
    
    # Создать временный ZIP файл
    zip_filename = f"{foldername}.zip"
    zip_path = os.path.join(UPLOAD_FOLDER, zip_filename)
    
    create_zip_from_folder(folder_path, zip_path)
    
    return send_file(zip_path, as_attachment=True, download_name=zip_filename)

@app.route("/delete/<path:filename>", methods=["DELETE"])
def delete(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    local_ip = get_local_ip()
    print("\n" + "="*50)
    print("🚀 LAN File Share Pro запущен!")
    print("="*50)
    print(f"📡 Локальный адрес: http://{local_ip}:8000")
    print(f"🏠 Локальный: http://localhost:8000")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=8000, debug=False)
