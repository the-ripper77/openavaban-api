import os
import sys
from http.server import BaseHTTPRequestHandler

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

BULK_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bulk Upload - openavaban-api</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📦</text></svg>">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0f;--surface:#14141f;--surface2:#1e1e2e;--border:#2a2a3a;--text:#e0e0e0;--text2:#888;--accent:#7c5cff;--success:#4caf50;--error:#ef5350}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}

.topbar{position:sticky;top:0;z-index:40;background:rgba(10,10,15,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:12px 32px;display:flex;align-items:center;gap:16px}
.logo{font-size:18px;font-weight:700;color:var(--accent);white-space:nowrap}.logo span{color:var(--text)}
.topbar-links{margin-left:auto;display:flex;gap:20px;font-size:14px}
.topbar-links a{color:var(--text2)}.topbar-links a:hover{color:var(--accent)}

.container{max-width:800px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:28px;font-weight:700;margin-bottom:8px}
.subtitle{color:var(--text2);margin-bottom:32px}

.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:24px;margin-bottom:20px}
.card h2{font-size:18px;font-weight:600;margin-bottom:12px}
.card p{color:var(--text2);font-size:14px;line-height:1.6;margin-bottom:12px}
.card ul{margin:8px 0 12px 20px;color:var(--text2);font-size:14px;line-height:1.6}

.download-btn{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:8px;background:var(--accent);color:#fff;border:none;cursor:pointer;font-size:14px;font-weight:600;transition:opacity .2s}
.download-btn:hover{opacity:.9}

.drop-zone{border:2px dashed var(--border);border-radius:12px;padding:48px 24px;text-align:center;cursor:pointer;transition:all .2s}
.drop-zone:hover,.drop-zone.dragover{border-color:var(--accent);background:rgba(124,92,255,.05)}
.drop-zone svg{width:48px;height:48px;color:var(--text2);margin-bottom:12px}
.drop-zone p{color:var(--text2);font-size:15px}
.drop-zone .filename{color:var(--accent);font-weight:600;margin-top:8px}
input[type="file"]{display:none}

.upload-btn{display:block;width:100%;padding:14px;border-radius:8px;background:var(--accent);color:#fff;border:none;cursor:pointer;font-size:15px;font-weight:600;margin-top:16px;transition:opacity .2s}
.upload-btn:hover{opacity:.9}
.upload-btn:disabled{opacity:.4;cursor:not-allowed}
.upload-btn.success{background:var(--success)}

.results{margin-top:24px}
.results-header{display:flex;gap:16px;margin-bottom:16px}
.stat{padding:12px 20px;border-radius:8px;background:var(--surface2);text-align:center;flex:1}
.stat .num{font-size:24px;font-weight:700}
.stat .label{font-size:12px;color:var(--text2);margin-top:4px}
.stat.success .num{color:var(--success)}
.stat.failed .num{color:var(--error)}

.result-list{max-height:300px;overflow-y:auto}
.result-item{display:flex;align-items:center;gap:12px;padding:10px 14px;border-bottom:1px solid var(--border);font-size:13px}
.result-item:last-child{border-bottom:none}
.result-row{color:var(--text2);min-width:40px}
.result-status{padding:2px 8px;border-radius:4px;font-size:11px;font-weight:600}
.result-status.ok{background:rgba(76,175,80,.15);color:var(--success)}
.result-status.error{background:rgba(239,83,80,.15);color:var(--error)}
.result-msg{color:var(--text2);flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

@media(max-width:600px){.results-header{flex-direction:column}}
</style>
</head>
<body>
<div class="topbar">
  <div class="logo">openavaban<span>-api</span></div>
  <div class="topbar-links">
    <a href="/">Home</a>
    <a href="/docs/bulk-upload">Docs</a>
    <a href="https://github.com/the-ripper77/openavaban-api" target="_blank" rel="noopener" title="GitHub">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
    </a>
  </div>
</div>

<div class="container">
  <h1>Bulk Upload</h1>
  <p class="subtitle">Upload up to 100 images at once using a CSV file.</p>

  <div class="card">
    <h2>1. Download Template</h2>
    <p>Download the CSV template, fill in your image URLs and metadata, then upload it below.</p>
    <button class="download-btn" onclick="downloadTemplate()">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
      Download CSV Template
    </button>
  </div>

  <div class="card">
    <h2>2. Upload CSV</h2>
    <p>Drag and drop your CSV file here, or click to browse.</p>
    <div class="drop-zone" id="dropZone">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
      <p>Drop CSV file here or click to browse</p>
      <div class="filename" id="fileName"></div>
    </div>
    <input type="file" id="fileInput" accept=".csv">
    <button class="upload-btn" id="uploadBtn" disabled>Upload Images</button>
  </div>

  <div class="results" id="results" style="display:none">
    <h2 style="margin-bottom:16px">Results</h2>
    <div class="results-header">
      <div class="stat"><div class="num" id="totalCount">0</div><div class="label">Total</div></div>
      <div class="stat success"><div class="num" id="successCount">0</div><div class="label">Success</div></div>
      <div class="stat failed"><div class="num" id="failedCount">0</div><div class="label">Failed</div></div>
    </div>
    <div class="card">
      <div class="result-list" id="resultList"></div>
    </div>
  </div>
</div>

<script>
const CSV_TEMPLATE = "file_url,name,class_type,category,tags\nhttps://example.com/photo1.jpg,Profile Photo,avatar,profile,\"main,profile\"\nhttps://example.com/banner1.png,Social Banner,banner,social,\"banner,v2\"\nhttps://example.com/photo2.png,Cute Avatar,avatar,profile,cute\n";

function downloadTemplate() {
  const blob = new Blob([CSV_TEMPLATE], { type: "text/csv" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "openavaban-bulk-template.csv";
  a.click();
  URL.revokeObjectURL(a.href);
}

const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const uploadBtn = document.getElementById("uploadBtn");
let selectedFile = null;

dropZone.onclick = () => fileInput.click();
dropZone.ondragover = (e) => { e.preventDefault(); dropZone.classList.add("dragover"); };
dropZone.ondragleave = () => dropZone.classList.remove("dragover");
dropZone.ondrop = (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  const file = e.dataTransfer.files[0];
  if (file && file.name.endsWith(".csv")) selectFile(file);
};
fileInput.onchange = () => { if (fileInput.files[0]) selectFile(fileInput.files[0]); };

function selectFile(file) {
  selectedFile = file;
  fileName.textContent = file.name + " (" + (file.size / 1024).toFixed(1) + " KB)";
  uploadBtn.disabled = false;
}

uploadBtn.onclick = async () => {
  if (!selectedFile) return;
  uploadBtn.disabled = true;
  uploadBtn.textContent = "Uploading...";
  uploadBtn.style.opacity = "0.6";
  document.getElementById("results").style.display = "none";

  const form = new FormData();
  form.append("file", selectedFile);

  try {
    const res = await fetch("/api/bulk", {
      method: "POST",
      body: form
    });
    const data = await res.json();
    showResults(data);
    selectedFile = null;
    fileName.textContent = "";
    uploadBtn.textContent = "Uploaded ✓";
    uploadBtn.style.opacity = "1";
    uploadBtn.style.background = "var(--success)";
    dropZone.style.display = "none";
  } catch (e) {
    alert("Upload failed: " + e.message);
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload Images";
    uploadBtn.style.opacity = "1";
  }
};

function showResults(data) {
  document.getElementById("results").style.display = "block";
  document.getElementById("totalCount").textContent = data.total || 0;
  document.getElementById("successCount").textContent = data.success || 0;
  document.getElementById("failedCount").textContent = data.failed || 0;

  const list = document.getElementById("resultList");
  list.innerHTML = "";
  (data.results || []).forEach(r => {
    const item = document.createElement("div");
    item.className = "result-item";
    item.innerHTML = `<span class="result-row">#${r.row}</span>
      <span class="result-status ${r.status}">${r.status}</span>
      <span class="result-msg">${r.url || r.error || ""}</span>`;
    list.appendChild(item);
  });

  const resetBtn = document.createElement("button");
  resetBtn.className = "download-btn";
  resetBtn.style.marginTop = "16px";
  resetBtn.textContent = "Upload another CSV";
  resetBtn.onclick = () => {
    selectedFile = null;
    fileName.textContent = "";
    uploadBtn.textContent = "Upload Images";
    uploadBtn.style.background = "";
    uploadBtn.style.opacity = "1";
    uploadBtn.disabled = true;
    dropZone.style.display = "";
    document.getElementById("results").style.display = "none";
  };
  document.getElementById("results").appendChild(resetBtn);
}
</script>
</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(BULK_HTML.encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()
