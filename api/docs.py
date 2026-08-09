import os
import sys
import markdown

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")

PAGES = [
    {"slug": "about", "title": "About", "section": "Introduction"},
    {"slug": "quickstart", "title": "Quick Start", "section": "Introduction"},
    {"slug": "search", "title": "Search Images", "section": "API Reference"},
    {"slug": "upload", "title": "Upload Image", "section": "API Reference"},
    {"slug": "profiles", "title": "Get / Update / Delete", "section": "API Reference"},
    {"slug": "random", "title": "Random Image", "section": "API Reference"},
    {"slug": "bulk-upload", "title": "Bulk Upload", "section": "API Reference"},
]

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#0a0a0f;--surface:#14141f;--surface2:#1e1e2e;--border:#2a2a3a;--text:#e0e0e0;--text2:#888;--accent:#7c5cff;--accent2:#5c3ddf;--code-bg:#1a1a2e}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;display:flex}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}

.sidebar{width:260px;min-height:100vh;background:var(--surface);border-right:1px solid var(--border);padding:20px 0;position:fixed;top:0;left:0;bottom:0;overflow-y:auto;z-index:50}
.sidebar-logo{padding:0 20px 20px;font-size:18px;font-weight:700;color:var(--accent);border-bottom:1px solid var(--border);margin-bottom:12px}
.sidebar-logo span{color:var(--text)}
.sidebar-logo a{color:inherit;text-decoration:none}
.nav-section{padding:12px 20px 4px;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.05em;color:var(--text2)}
.nav-link{display:block;padding:6px 20px 6px 28px;font-size:14px;color:var(--text2);text-decoration:none;transition:all .15s}
.nav-link:hover{color:var(--text);background:var(--hover)}
.nav-link.active{color:var(--accent);background:rgba(124,92,255,.1);border-right:2px solid var(--accent)}
.sidebar-footer{position:absolute;bottom:0;left:0;right:0;padding:16px 20px;border-top:1px solid var(--border);font-size:12px;color:var(--text2)}
.sidebar-footer a{color:var(--text2)}.sidebar-footer a:hover{color:var(--accent)}

.main{margin-left:260px;flex:1;min-height:100vh}
.topbar{position:sticky;top:0;z-index:40;background:rgba(10,10,15,.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:12px 32px;display:flex;align-items:center;gap:16px}
.topbar-links{margin-left:auto;display:flex;gap:20px;font-size:14px}
.topbar-links a{color:var(--text2)}.topbar-links a:hover{color:var(--accent)}
.topbar-links a.active{color:var(--accent)}

.content{max-width:820px;margin:0 auto;padding:40px 48px 80px}
.content h1{font-size:32px;font-weight:700;margin-bottom:8px}
.content h2{font-size:22px;font-weight:600;margin:32px 0 12px;padding-top:16px;border-top:1px solid var(--border)}
.content h3{font-size:17px;font-weight:600;margin:24px 0 8px}
.content p{margin:10px 0;line-height:1.7;color:var(--text)}
.content ul,.content ol{margin:10px 0 10px 24px;line-height:1.7}
.content li{margin:4px 0}
.content strong{color:#fff}
.content code{background:var(--code-bg);padding:2px 6px;border-radius:4px;font-size:13px;font-family:'SF Mono',Monaco,Consolas,monospace;color:#e06c75}
.content pre{background:var(--code-bg);border:1px solid var(--border);border-radius:8px;padding:16px 20px;margin:14px 0;overflow-x:auto;line-height:1.5}
.content pre code{background:none;padding:0;color:var(--text);font-size:13px}
.content table{width:100%;border-collapse:collapse;margin:14px 0;font-size:14px}
.content th,.content td{padding:10px 14px;border:1px solid var(--border);text-align:left}
.content th{background:var(--surface2);font-weight:600;color:#fff}
.content td{color:var(--text)}
.content blockquote{border-left:3px solid var(--accent);padding:10px 16px;margin:14px 0;background:rgba(124,92,255,.05);border-radius:0 8px 8px 0;color:var(--text2)}
.content hr{border:none;border-top:1px solid var(--border);margin:28px 0}

@media(max-width:800px){
  .sidebar{transform:translateX(-100%);transition:transform .2s}
  .sidebar.open{transform:translateX(0)}
  .main{margin-left:0}
  .content{padding:24px 20px 60px}
  .menu-btn{display:block!important}
}
.menu-btn{display:none;position:fixed;bottom:20px;right:20px;width:48px;height:48px;border-radius:50%;background:var(--accent);color:#fff;border:none;cursor:pointer;font-size:22px;z-index:100;box-shadow:0 4px 20px rgba(124,92,92,.4)}
"""

JS = r"""
document.querySelector('.menu-btn')?.addEventListener('click',()=>{
  document.querySelector('.sidebar').classList.toggle('open')
});
document.addEventListener('click',(e)=>{
  const sb=document.querySelector('.sidebar');
  const btn=document.querySelector('.menu-btn');
  if(sb&&btn&&!sb.contains(e.target)&&!btn.contains(e.target)){
    sb.classList.remove('open')
  }
});
"""


def render_page(current_slug):
    sections = {}
    for p in PAGES:
        sections.setdefault(p["section"], []).append(p)

    nav_html = ""
    for section, pages in sections.items():
        nav_html += f'<div class="nav-section">{section}</div>\n'
        for p in pages:
            active = " active" if p["slug"] == current_slug else ""
            nav_html += f'<a class="nav-link{active}" href="/docs/{p["slug"]}">{p["title"]}</a>\n'

    md_path = os.path.join(DOCS_DIR, f"{current_slug}.md")
    if not os.path.exists(md_path):
        md_path = os.path.join(DOCS_DIR, "about.md")
        current_slug = "about"

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "codehilite"],
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Docs - openavaban-api</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📖</text></svg>">
<style>{CSS}</style>
</head>
<body>

<nav class="sidebar">
  <div class="sidebar-logo"><a href="/docs/about">openavaban<span>-api</span></a></div>
  {nav_html}
  <div class="sidebar-footer">
    <a href="/">Home</a> &middot; <a href="https://github.com/the-ripper77/openavaban-api" target="_blank" rel="noopener">GitHub</a>
  </div>
</nav>

<div class="main">
  <div class="topbar">
    <div class="topbar-links">
      <a href="/">Home</a>
      <a href="/docs/about" class="active">Docs</a>
      <a href="https://github.com/the-ripper77/openavaban-api" target="_blank" rel="noopener" title="GitHub">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
      </a>
    </div>
  </div>
  <div class="content">{html_content}</div>
</div>

<button class="menu-btn">&#9776;</button>
<script>{JS}</script>
</body>
</html>"""


class handler:
    def __init__(self, req=None, res=None):
        pass

    def do_GET(self):
        from http.server import BaseHTTPRequestHandler
        path = self.path if hasattr(self, "path") else "/"

        slug = path.strip("/").split("/")[-1] if path.strip("/") else "about"
        slug = slug or "about"

        valid_slugs = [p["slug"] for p in PAGES]
        if slug not in valid_slugs:
            slug = "about"

        html = render_page(slug)

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())
