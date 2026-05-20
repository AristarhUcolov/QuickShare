/* QuickShare — front-end logic */
"use strict";

/* ── Translations ──────────────────────────────────────── */
const I18N = {
  en: {
    subtitle: "Local network file transfer",
    files: "Files", total: "Total",
    dropTitle: "Drop files here",
    dropDesc: "or pick files and folders to share",
    selectFiles: "Select files", selectFolder: "Select folder",
    searchPlaceholder: "Search files…",
    sortName: "Name", sortSize: "Size", sortDate: "Date",
    emptyTitle: "No files yet",
    emptyDesc: "Upload your first file to get started",
    uploading: "Uploading…",
    qrTitle: "Scan to connect",
    qrDesc: "Open this address on any device in your network",
    copy: "Copy address", close: "Close", cancel: "Cancel", delete: "Delete",
    confirmTitle: "Delete item?",
    download: "Download", zip: "ZIP",
    folder: "Folder",
    confirmText: name => `“${name}” will be removed permanently.`,
    uploadingN: n => `Uploading ${n} item(s)…`,
    uploaded: n => `${n} item(s) uploaded`,
    deleted: name => `“${name}” deleted`,
    copied: "Address copied",
    failed: "Something went wrong",
  },
  ru: {
    subtitle: "Передача файлов по локальной сети",
    files: "Файлов", total: "Объём",
    dropTitle: "Перетащите файлы сюда",
    dropDesc: "или выберите файлы и папки для передачи",
    selectFiles: "Выбрать файлы", selectFolder: "Выбрать папку",
    searchPlaceholder: "Поиск файлов…",
    sortName: "Имя", sortSize: "Размер", sortDate: "Дата",
    emptyTitle: "Пока нет файлов",
    emptyDesc: "Загрузите первый файл, чтобы начать",
    uploading: "Загрузка…",
    qrTitle: "Сканируйте для подключения",
    qrDesc: "Откройте этот адрес на любом устройстве в сети",
    copy: "Копировать адрес", close: "Закрыть", cancel: "Отмена", delete: "Удалить",
    confirmTitle: "Удалить элемент?",
    download: "Скачать", zip: "ZIP",
    folder: "Папка",
    confirmText: name => `«${name}» будет удалён безвозвратно.`,
    uploadingN: n => `Загрузка ${n} элемент(ов)…`,
    uploaded: n => `Загружено элементов: ${n}`,
    deleted: name => `«${name}» удалён`,
    copied: "Адрес скопирован",
    failed: "Что-то пошло не так",
  },
};

let lang = localStorage.getItem("qs-lang") || "en";
let theme = localStorage.getItem("qs-theme") || "dark";
let sortKey = "name";
let entries = [];

const $ = sel => document.querySelector(sel);
const t = () => I18N[lang];

/* ── i18n + theme application ──────────────────────────── */
function applyI18n() {
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const v = t()[el.dataset.i18n];
    if (typeof v === "string") el.textContent = v;
  });
  document.querySelectorAll("[data-i18n-ph]").forEach(el => {
    el.placeholder = t()[el.dataset.i18nPh];
  });
  $("#langBtn").textContent = lang === "en" ? "RU" : "EN";
  render();
}

function applyTheme() {
  document.documentElement.dataset.theme = theme;
  $("#themeBtn").textContent = theme === "dark" ? "☾" : "☀";
}

/* ── Helpers ───────────────────────────────────────────── */
function formatSize(bytes) {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let n = bytes, i = 0;
  while (n >= 1024 && i < units.length - 1) { n /= 1024; i++; }
  return `${n < 10 && i > 0 ? n.toFixed(1) : Math.round(n)} ${units[i]}`;
}

function formatDate(unix) {
  return new Date(unix * 1000).toLocaleString(lang === "ru" ? "ru-RU" : "en-GB", {
    day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

// Pick an icon glyph + accent colour from a file's extension.
const ICONS = [
  { ext: ["png","jpg","jpeg","gif","webp","svg","bmp"], glyph: "IMG", color: "#c9824f" },
  { ext: ["mp4","mkv","mov","avi","webm"],              glyph: "VID", color: "#bd5f6b" },
  { ext: ["mp3","wav","flac","ogg","m4a"],              glyph: "AUD", color: "#8a73b4" },
  { ext: ["zip","rar","7z","tar","gz"],                 glyph: "ZIP", color: "#b6953f" },
  { ext: ["pdf"],                                       glyph: "PDF", color: "#bd5f6b" },
  { ext: ["doc","docx","txt","md","rtf"],               glyph: "DOC", color: "#527fb4" },
  { ext: ["xls","xlsx","csv"],                          glyph: "XLS", color: "#4f9b78" },
  { ext: ["js","ts","go","py","html","css","json","c","cpp"], glyph: "<>", color: "#6168a8" },
  { ext: ["exe","msi","apk","dmg"],                     glyph: "APP", color: "#7c8089" },
];
function iconFor(entry) {
  if (entry.isDir) return { glyph: "DIR", color: "#b6953f" };
  const ext = entry.name.split(".").pop().toLowerCase();
  return ICONS.find(i => i.ext.includes(ext)) || { glyph: "FILE", color: "#5d6470" };
}

/* ── Rendering ─────────────────────────────────────────── */
function render() {
  const query = $("#search").value.trim().toLowerCase();
  let list = entries.filter(e => e.name.toLowerCase().includes(query));

  list.sort((a, b) => {
    if (a.isDir !== b.isDir) return a.isDir ? -1 : 1;
    if (sortKey === "size") return b.size - a.size;
    if (sortKey === "date") return b.modified - a.modified;
    return a.name.localeCompare(b.name);
  });

  const grid = $("#grid");
  grid.innerHTML = "";
  $("#empty").classList.toggle("hidden", entries.length !== 0);

  for (const e of list) {
    const ic = iconFor(e);
    const card = document.createElement("div");
    card.className = "card";
    const dl = e.isDir
      ? `/api/zip?path=${encodeURIComponent(e.name)}`
      : `/api/download?path=${encodeURIComponent(e.name)}`;
    card.innerHTML = `
      <div class="card-top">
        <div class="card-icon" style="background:${ic.color}">${ic.glyph}</div>
        <div class="card-name"></div>
      </div>
      <div class="card-meta">
        <span>${formatSize(e.size)}</span>
        <span>${formatDate(e.modified)}</span>
      </div>
      <div class="card-actions">
        <a class="btn btn-primary" href="${dl}">↓ ${e.isDir ? t().zip : t().download}</a>
        <button class="btn btn-danger" data-del="${encodeURIComponent(e.name)}">✕</button>
      </div>`;
    card.querySelector(".card-name").textContent = e.name;
    card.querySelector("[data-del]").addEventListener("click", () => confirmDelete(e.name));
    grid.appendChild(card);
  }
}

async function loadFiles() {
  try {
    const res = await fetch("/api/files");
    const data = await res.json();
    entries = data.files || [];
    $("#statCount").textContent = data.count || 0;
    $("#statSize").textContent = formatSize(data.totalSize || 0);
    render();
  } catch {
    toast(t().failed, "error");
  }
}

/* ── Upload ────────────────────────────────────────────── */
function upload(fileList) {
  const files = [...fileList];
  if (!files.length) return;

  const form = new FormData();
  // webkitRelativePath preserves folder structure when a folder is picked.
  for (const f of files) form.append("files", f, f.webkitRelativePath || f.name);

  const card = $("#uploadCard");
  card.classList.remove("hidden");
  $("#uploadLabel").textContent = t().uploadingN(files.length);

  const xhr = new XMLHttpRequest();
  xhr.upload.addEventListener("progress", e => {
    if (!e.lengthComputable) return;
    const pct = Math.round((e.loaded / e.total) * 100);
    $("#uploadBar").style.width = pct + "%";
    $("#uploadPercent").textContent = pct + "%";
  });
  xhr.addEventListener("load", () => {
    card.classList.add("hidden");
    $("#uploadBar").style.width = "0%";
    $("#uploadPercent").textContent = "0%";
    if (xhr.status === 200) {
      const n = JSON.parse(xhr.responseText).count || files.length;
      toast(t().uploaded(n), "ok");
      loadFiles();
    } else {
      toast(t().failed, "error");
    }
  });
  xhr.addEventListener("error", () => {
    card.classList.add("hidden");
    toast(t().failed, "error");
  });
  xhr.open("POST", "/api/upload");
  xhr.send(form);
}

/* ── Delete ────────────────────────────────────────────── */
let pendingDelete = null;
function confirmDelete(name) {
  pendingDelete = name;
  $("#confirmText").textContent = t().confirmText(name);
  $("#confirmModal").classList.remove("hidden");
}
async function doDelete() {
  const name = pendingDelete;
  $("#confirmModal").classList.add("hidden");
  if (!name) return;
  try {
    const res = await fetch("/api/delete?path=" + encodeURIComponent(name), { method: "DELETE" });
    if (res.ok) { toast(t().deleted(name), "ok"); loadFiles(); }
    else toast(t().failed, "error");
  } catch {
    toast(t().failed, "error");
  }
  pendingDelete = null;
}

/* ── Toasts ────────────────────────────────────────────── */
function toast(msg, kind = "") {
  const el = document.createElement("div");
  el.className = "toast " + kind;
  el.textContent = msg;
  $("#toasts").appendChild(el);
  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transition = "opacity 0.3s";
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

/* ── QR modal ──────────────────────────────────────────── */
function openQR() {
  const url = `${location.protocol}//${location.host}`;
  $("#qrImage").src = "/api/qr?_=" + Date.now();
  $("#qrUrl").textContent = url;
  $("#qrModal").classList.remove("hidden");
}

/* ── Wiring ────────────────────────────────────────────── */
function init() {
  applyTheme();
  applyI18n();
  loadFiles();

  $("#fileInput").addEventListener("change", e => upload(e.target.files));
  $("#folderInput").addEventListener("change", e => upload(e.target.files));

  const dz = $("#dropzone");
  dz.addEventListener("click", e => {
    if (!e.target.closest("label")) $("#fileInput").click();
  });
  ["dragenter", "dragover"].forEach(ev =>
    dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.add("drag"); }));
  ["dragleave", "drop"].forEach(ev =>
    dz.addEventListener(ev, e => { e.preventDefault(); dz.classList.remove("drag"); }));
  dz.addEventListener("drop", e => upload(e.dataTransfer.files));

  $("#search").addEventListener("input", render);

  document.querySelectorAll(".chip").forEach(chip =>
    chip.addEventListener("click", () => {
      document.querySelectorAll(".chip").forEach(c => c.classList.remove("is-active"));
      chip.classList.add("is-active");
      sortKey = chip.dataset.sort;
      render();
    }));

  $("#langBtn").addEventListener("click", () => {
    lang = lang === "en" ? "ru" : "en";
    localStorage.setItem("qs-lang", lang);
    applyI18n();
  });
  $("#themeBtn").addEventListener("click", () => {
    theme = theme === "dark" ? "light" : "dark";
    localStorage.setItem("qs-theme", theme);
    applyTheme();
  });

  $("#qrBtn").addEventListener("click", openQR);
  $("#qrClose").addEventListener("click", () => $("#qrModal").classList.add("hidden"));
  $("#qrModal").addEventListener("click", e => {
    if (e.target.id === "qrModal") $("#qrModal").classList.add("hidden");
  });
  $("#qrCopy").addEventListener("click", async () => {
    try {
      await navigator.clipboard.writeText($("#qrUrl").textContent);
      toast(t().copied, "ok");
    } catch { toast(t().failed, "error"); }
  });

  $("#confirmOk").addEventListener("click", doDelete);
  $("#confirmCancel").addEventListener("click", () => $("#confirmModal").classList.add("hidden"));
  $("#confirmModal").addEventListener("click", e => {
    if (e.target.id === "confirmModal") $("#confirmModal").classList.add("hidden");
  });

  document.addEventListener("keydown", e => {
    if (e.key === "Escape") {
      $("#qrModal").classList.add("hidden");
      $("#confirmModal").classList.add("hidden");
    }
  });

  // Refresh listing periodically so multiple devices stay in sync.
  setInterval(loadFiles, 5000);
}

document.addEventListener("DOMContentLoaded", init);
