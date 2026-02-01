from flask import Flask, request, send_from_directory, render_template_string, redirect, url_for
import os

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>LAN File Share</title>
<style>
body { font-family: Arial; background:#f4f4f4; padding:20px; }
.container { background:white; padding:20px; max-width:600px; margin:auto; border-radius:8px; }
h2 { margin-top:0; }
ul { padding-left:20px; }
li { margin:6px 0; }
a { text-decoration:none; color:#0066cc; }
a:hover { text-decoration:underline; }
</style>
</head>
<body>
<div class="container">
<h2>📁 Файлы на ноутбуке</h2>

<form action="/upload" method="post" enctype="multipart/form-data">
  <input type="file" name="file" required>
  <button type="submit">Загрузить на ноутбук</button>
</form>

<hr>

<ul>
{% if files %}
  {% for f in files %}
    <li>⬇ <a href="/download/{{ f }}">{{ f }}</a></li>
  {% endfor %}
{% else %}
  <li>Файлов пока нет</li>
{% endif %}
</ul>

</div>
</body>
</html>
"""

@app.route("/")
def index():
    files = sorted(os.listdir(UPLOAD_FOLDER))
    return render_template_string(HTML, files=files)

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if file:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return redirect(url_for("index"))

@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
