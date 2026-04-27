import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add Light Theme Tokens
LIGHT_TOKENS = """
:root[data-theme="light"] {
  --white: #ffffff;
  --bg: #f9f8f6;
  --bg2: #f2f1ee;
  --bg3: #eae9e5;
  --line: #ececea;
  --line2: #dddcda;
  --text: #1a1916;
  --text2: #6b6963;
  --text3: #b0aca6;
  --accent: #2563eb;
  --accent-bg: rgba(37,99,235,.07);
  --shadow-pop: 0 12px 32px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.05);
  --shadow-row: 0 4px 16px rgba(0,0,0,0.05);
  --idea-bg: rgba(109, 40, 217, 0.1); --idea-fg: #6d28d9;
  --building-bg: rgba(194, 87, 10, 0.1); --building-fg: #c2570a;
  --completed-bg: rgba(22, 101, 52, 0.1); --completed-fg: #166534;
  --shipped-bg: rgba(30, 64, 175, 0.1); --shipped-fg: #1e40af;
  --dropped-bg: rgba(120, 113, 108, 0.1); --dropped-fg: #78716c;
}
:root[data-theme="light"] body, :root[data-theme="light"] .app {
  background-image: none;
}
:root[data-theme="light"] .topbar {
  background: rgba(249, 248, 246, 0.85);
  border-bottom: 1px solid var(--line2);
}
:root[data-theme="light"] thead tr {
  background: rgba(249, 248, 246, 0.95);
}
:root[data-theme="light"] .tb-search {
  background: var(--white);
}
:root[data-theme="light"] .tb-btn {
  background: var(--white);
  border-color: var(--line2);
  color: var(--text2);
}
:root[data-theme="light"] .cinp, :root[data-theme="light"] .cat-sel, :root[data-theme="light"] .name-edit-wrap {
  background: var(--white);
}
:root[data-theme="light"] td.cell-focus::after {
  box-shadow: inset 0 0 0 2px var(--accent);
}
:root[data-theme="light"] .sdrop, :root[data-theme="light"] .tech-pop, :root[data-theme="light"] .time-pop, :root[data-theme="light"] .export-menu {
  background: var(--white);
  border: 1px solid var(--line2);
}
:root[data-theme="light"] .tp-inp, :root[data-theme="light"] .tp-inp-h, :root[data-theme="light"] .sf-inp, :root[data-theme="light"] .sf-sel {
  background: var(--white);
}
:root[data-theme="light"] .sheet, :root[data-theme="light"] .login-box, :root[data-theme="light"] .cmd-box {
  background: var(--white);
}
:root[data-theme="light"] .cmd-ft, :root[data-theme="light"] .filterbar {
  background: var(--bg2);
}
:root[data-theme="light"] .tb-name { text-shadow: none; }
:root[data-theme="light"] td.td-num { background: transparent; }
:root[data-theme="light"] th.th-num { background: transparent; }
"""

html = html.replace('</style>', LIGHT_TOKENS + '\n</style>')

# 2. Add Toggle Button in topbar
btn_html = """
      <button class="tb-btn" onclick="toggleTheme()" id="theme-btn" title="Toggle Theme">☀️</button>
      <button class="tb-btn" id="admin-btn" onclick="toggleAdmin()">🔐 Admin</button>"""
html = html.replace('<button class="tb-btn" id="admin-btn" onclick="toggleAdmin()">🔐 Admin</button>', btn_html)

# 3. Add JS functions
js_html = """
// ═══════════════════════════════════════════
// THEME
// ═══════════════════════════════════════════
function toggleTheme() {
  const root = document.documentElement;
  const isLight = root.getAttribute('data-theme') === 'light';
  const newTheme = isLight ? 'dark' : 'light';
  root.setAttribute('data-theme', newTheme);
  localStorage.setItem('devden-theme', newTheme);
  document.getElementById('theme-btn').textContent = newTheme === 'light' ? '🌙' : '☀️';
}
function initTheme() {
  const saved = localStorage.getItem('devden-theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
  const btn = document.getElementById('theme-btn');
  if(btn) btn.textContent = saved === 'light' ? '🌙' : '☀️';
}
initTheme();

// ═══════════════════════════════════════════
// STATE
"""
html = html.replace('// ═══════════════════════════════════════════\n// STATE', js_html)

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Theme toggle added!")
