import re

with open("templates/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. NEW CSS (Dark Glassmorphism Modern Excel)
NEW_CSS = """<style>
/* ═══════════════════════════════════════════════
   TOKENS (Modern Dark Glassmorphism)
═══════════════════════════════════════════════ */
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --white: rgba(255, 255, 255, 0.03);
  --bg: #08090d;
  --bg2: #11131a;
  --bg3: #1c1f2b;
  --line: rgba(255, 255, 255, 0.06);
  --line2: rgba(255, 255, 255, 0.12);
  --text: #f8fafc;
  --text2: #94a3b8;
  --text3: #475569;
  --accent: #38bdf8;
  --accent-bg: rgba(56, 189, 248, 0.15);
  --f: 'Inter', system-ui, sans-serif;
  --mono: 'JetBrains Mono', monospace;
  --row-h: 46px;
  --th-h: 36px;
  --r: 8px;
  --r-sm: 6px;
  --shadow-pop: 0 12px 32px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08);
  --shadow-row: 0 4px 16px rgba(0,0,0,0.4);
  
  --idea-bg: rgba(139, 92, 246, 0.15); --idea-fg: #d8b4fe;
  --building-bg: rgba(245, 158, 11, 0.15); --building-fg: #fcd34d;
  --completed-bg: rgba(16, 185, 129, 0.15); --completed-fg: #6ee7b7;
  --shipped-bg: rgba(56, 189, 248, 0.15); --shipped-fg: #7dd3fc;
  --dropped-bg: rgba(100, 116, 139, 0.15); --dropped-fg: #cbd5e1;
}
html,body{height:100%;background:var(--bg);color:var(--text);font-family:var(--f);font-size:13.5px;line-height:1.5;-webkit-font-smoothing:antialiased}
input,select,textarea,button{font-family:var(--f)}
::placeholder{color:var(--text3)}
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button{-webkit-appearance:none;margin:0}
input[type=number]{-moz-appearance:textfield}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--line2);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--text3)}
.hidden { display: none !important; }

/* ═══════════════════════════════════════════════
   SHELL & TOPBAR
═══════════════════════════════════════════════ */
.app{display:flex;flex-direction:column;height:100vh;overflow:hidden;background:var(--bg);
  background-image: radial-gradient(circle at 50% 0%, rgba(56, 189, 248, 0.05), transparent 60%);
}
.topbar{
  height:54px;flex-shrink:0;display:flex;align-items:center;
  padding:0 24px;gap:16px;
  background:rgba(8, 9, 13, 0.7);
  backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);
  border-bottom:1px solid var(--line);z-index:60;position:relative;
}
.tb-name{
  font-size:22px;font-weight:800;color:var(--text);
  letter-spacing:-.04em;flex-shrink:0;line-height:1;
  text-shadow: 0 0 16px rgba(255,255,255,0.2);
}
.tb-div{width:1px;height:20px;background:var(--line2);flex-shrink:0}
.tb-stats{display:flex;align-items:center;gap:12px}
.tbs{font-size:12.5px;color:var(--text2)}
.tbs strong{color:var(--text);font-weight:600}
.tbs-dot{width:4px;height:4px;border-radius:50%;background:var(--line2)}
.tb-right{margin-left:auto;display:flex;align-items:center;gap:10px}
.tb-search{
  height:32px;padding:0 12px 0 32px;border-radius:16px;
  border:1px solid var(--line2);background:rgba(255,255,255,0.02);color:var(--text);
  font-size:13px;outline:none;width:200px;transition:0.25s cubic-bezier(0.4, 0, 0.2, 1);
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748b' stroke-width='2.5'%3E%3Ccircle cx='11' cy='11' r='8'/%3E%3Cpath d='m21 21-4.35-4.35'/%3E%3C/svg%3E");
  background-repeat:no-repeat;background-position:12px center;
}
.tb-search:focus{width:260px;background:rgba(255,255,255,0.06);border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-bg)}
.tb-btn{
  height:32px;padding:0 14px;border-radius:var(--r-sm);border:1px solid var(--line2);
  background:rgba(255,255,255,0.03);color:var(--text2);font-size:12.5px;font-weight:500;
  cursor:pointer;display:inline-flex;align-items:center;gap:6px;white-space:nowrap;transition:0.15s;
}
.tb-btn:hover{background:rgba(255,255,255,0.08);color:var(--text);border-color:rgba(255,255,255,0.2)}
.tb-btn.ink{background:var(--accent);color:#fff;border-color:var(--accent);font-weight:600;text-shadow:0 1px 2px rgba(0,0,0,0.2)}
.tb-btn.ink:hover{background:#0ea5e9;box-shadow:0 0 12px var(--accent-bg)}
.admin-dot{width:6px;height:6px;border-radius:50%;background:#10b981;flex-shrink:0;box-shadow:0 0 8px #10b981}

.export-wrap{position:relative}
.export-menu{
  position:absolute;top:calc(100% + 8px);right:0;
  background:#14161d;border:1px solid var(--line2);border-radius:var(--r);
  box-shadow:var(--shadow-pop);z-index:300;padding:6px;min-width:180px;display:none;
}
.export-menu.open{display:block;animation:fadeIn 0.15s ease-out}
.em-item{
  display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:6px;
  font-size:13px;color:var(--text2);cursor:pointer;text-decoration:none;transition:0.1s;
}
.em-item:hover{background:rgba(255,255,255,0.05);color:var(--text)}

/* ═══════════════════════════════════════════════
   FILTER BAR
═══════════════════════════════════════════════ */
.filterbar{
  height:44px;flex-shrink:0;display:flex;align-items:center;
  padding:0 24px;gap:6px;border-bottom:1px solid var(--line);background:rgba(0,0,0,0.2);
}
.fp{
  height:28px;padding:0 12px;border-radius:14px;border:1px solid transparent;
  background:transparent;color:var(--text2);font-size:12.5px;font-weight:500;
  cursor:pointer;transition:0.15s;white-space:nowrap;display:inline-flex;align-items:center;gap:6px;
}
.fp:hover{background:rgba(255,255,255,0.05);color:var(--text)}
.fp.on{background:var(--white);border-color:var(--line2);color:var(--text);font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,0.2)}
.fp-badge{
  font-size:10px;font-weight:700;font-family:var(--mono);
  background:rgba(255,255,255,0.08);color:var(--text2);border-radius:10px;
  padding:0 6px;min-width:18px;text-align:center;line-height:18px;
}
.fp.on .fp-badge{background:var(--accent);color:#08090d}
.fb-sep{width:1px;height:18px;background:var(--line);margin:0 4px}
.fb-right{margin-left:auto;display:flex;align-items:center;gap:12px}
.fb-count{font-size:12px;color:var(--text3);font-family:var(--mono)}
.sort-info{font-size:12px;color:var(--text3);display:flex;align-items:center;gap:6px}
.sort-clear{font-size:11px;color:var(--accent);cursor:pointer;text-decoration:underline;text-underline-offset:2px}

/* ═══════════════════════════════════════════════
   TABLE (Modern Grid)
═══════════════════════════════════════════════ */
.tbl-outer{flex:1;overflow:auto;position:relative}
table{width:100%;border-collapse:separate;border-spacing:0;table-layout:fixed;min-width:1200px}
thead{position:sticky;top:0;z-index:40}
thead tr{background:rgba(17, 19, 26, 0.95);backdrop-filter:blur(8px)}
th{
  height:var(--th-h);padding:0 14px;
  font-size:11px;font-weight:600;color:var(--text2);
  text-transform:uppercase;letter-spacing:0.06em;
  border-bottom:1px solid var(--line2);border-right:1px solid var(--line);
  text-align:left;white-space:nowrap;user-select:none;
}
th:last-child{border-right:none}
th.th-num{text-align:center;padding:0;background:rgba(255,255,255,0.01);width:48px}
th.th-ctr{text-align:center}
th.sortable{cursor:pointer;transition:0.1s}
th.sortable:hover{color:var(--text);background:rgba(255,255,255,0.02)}
th.sort-asc::after{content:' ↑';color:var(--accent)}
th.sort-desc::after{content:' ↓';color:var(--accent)}

/* rows */
tbody tr{transition:all 0.15s ease;position:relative;cursor:default}
tbody tr td { border-bottom: 1px solid var(--line); }
tbody tr.r-Building td{background:linear-gradient(to right,rgba(245,158,11,0.03),transparent 40%)}
tbody tr.r-Completed td{background:linear-gradient(to right,rgba(16,185,129,0.03),transparent 40%)}
tbody tr.r-Shipped td{background:linear-gradient(to right,rgba(56,189,248,0.03),transparent 40%)}
tbody tr.r-Dropped td{opacity:0.5}
tbody tr.r-Dropped:hover td{opacity:1}
tbody tr:hover td{background:var(--white);border-bottom-color:var(--line2)}
tbody tr.drag-over td{border-top:2px solid var(--accent)}
tbody tr.dragging td{opacity:0.4;background:var(--bg2)}

/* cells */
td{height:var(--row-h);padding:0;border-right:1px solid var(--line);vertical-align:middle;position:relative;overflow:visible}
td:last-child{border-right:none}
td.td-num{text-align:center;font-size:11px;color:var(--text3);font-family:var(--mono);background:rgba(255,255,255,0.01);border-right:1px solid var(--line2);width:48px;overflow:visible}
tbody tr:hover td.td-num{color:var(--text);background:rgba(255,255,255,0.04)}

td.cell-focus::after{content:'';position:absolute;inset:0;border:2px solid var(--accent);pointer-events:none;z-index:6;box-shadow:inset 0 0 10px var(--accent-bg)}

/* inline input */
.cinp{
  position:absolute;inset:0;width:100%;height:100%;
  padding:0 14px;border:none;outline:none;
  font-size:13.5px;font-family:var(--f);color:var(--text);
  background:#14161d;box-shadow:inset 0 0 0 2px var(--accent);z-index:20;
}

/* empty / add rows */
tr.empty-r td{height:var(--row-h)}
tr.add-r td{height:40px;cursor:pointer;border-bottom:1px dashed var(--line2)}
tr.add-r:hover td{background:var(--accent-bg);border-bottom-color:var(--accent)}
.add-r-label{display:flex;align-items:center;gap:8px;height:40px;padding:0 14px;font-size:13px;color:var(--text2);font-weight:500}
tr.add-r:hover .add-r-label{color:var(--accent)}

/* ═══════════════════════════════════════════════
   CELL COMPONENTS
═══════════════════════════════════════════════ */
.drag-handle{
  position:absolute;left:0;top:0;bottom:0;width:20px;
  display:flex;align-items:center;justify-content:center;
  color:var(--text3);font-size:14px;cursor:grab;opacity:0;transition:0.15s;z-index:3;
}
tbody tr:hover .drag-handle{opacity:1;color:var(--text2)}
.drag-handle:active{cursor:grabbing}
.num-wrap{display:flex;align-items:center;justify-content:center;height:100%;position:relative}

.name-wrap{display:flex;flex-direction:column;justify-content:center;padding:6px 14px;height:100%;cursor:text;min-width:0;transition:0.1s}
.name-wrap:hover{background:rgba(255,255,255,0.03)}
.name-main{display:flex;align-items:center;gap:8px;min-width:0}
.name-text{font-size:14px;font-weight:600;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.flagship-pip{display:inline-flex;align-items:center;font-size:10px;font-weight:700;padding:2px 6px;border-radius:4px;background:rgba(245,158,11,0.15);color:#fcd34d;border:1px solid rgba(245,158,11,0.3);flex-shrink:0;letter-spacing:0.04em;cursor:pointer;box-shadow:0 0 8px rgba(245,158,11,0.1)}
.flagship-pip:hover{background:rgba(245,158,11,0.25);border-color:#fcd34d}
.no-flagship-pip{display:none;font-size:12px;color:var(--text3);cursor:pointer;flex-shrink:0;transition:0.1s}
.no-flagship-pip:hover{color:#fcd34d;transform:scale(1.2)}
.name-wrap:hover .no-flagship-pip{display:inline-flex}
.name-desc{font-size:12px;color:var(--text2);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.4}

.name-edit-wrap{
  position:absolute;inset:0;z-index:20;background:#14161d;
  box-shadow:inset 0 0 0 2px var(--accent);
  display:flex;flex-direction:column;padding:4px 14px;gap:2px;justify-content:center;
}
.name-edit-wrap input{border:none;outline:none;background:transparent;font-family:var(--f);color:var(--text);padding:0;width:100%}
.ne-name{font-size:14px;font-weight:600}
.ne-desc{font-size:12px;color:var(--text2)}

.sc-wrap{display:flex;align-items:center;padding:0 12px;height:100%;position:relative}
.spill{
  display:inline-flex;align-items:center;gap:6px;
  font-size:12px;font-weight:600;padding:4px 10px;border-radius:20px;
  white-space:nowrap;cursor:pointer;transition:0.15s;user-select:none;
  border:1px solid rgba(255,255,255,0.05);
}
.spill:hover{filter:brightness(1.2);transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,0.2)}
.spill::before{content:'';width:6px;height:6px;border-radius:50%;background:currentColor;flex-shrink:0;box-shadow:0 0 6px currentColor}
.sp-Idea     {background:var(--idea-bg);     color:var(--idea-fg); border-color:rgba(139, 92, 246, 0.3)}
.sp-Building {background:var(--building-bg); color:var(--building-fg); border-color:rgba(245, 158, 11, 0.3)}
.sp-Completed{background:var(--completed-bg);color:var(--completed-fg); border-color:rgba(16, 185, 129, 0.3)}
.sp-Shipped  {background:var(--shipped-bg);  color:var(--shipped-fg); border-color:rgba(56, 189, 248, 0.3)}
.sp-Dropped  {background:var(--dropped-bg);  color:var(--dropped-fg); border-color:rgba(100, 116, 139, 0.3)}

.sdrop{
  position:absolute;top:calc(100% + 6px);left:12px;
  background:#14161d;border:1px solid var(--line2);
  border-radius:12px;box-shadow:var(--shadow-pop);
  z-index:500;padding:6px;min-width:160px;animation:fadeIn 0.1s ease-out;
}
.sdi{display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);transition:0.1s}
.sdi:hover{background:rgba(255,255,255,0.05);color:var(--text)}
.sdi-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;box-shadow:0 0 6px currentColor}
.sdi.active{background:rgba(255,255,255,0.08);color:var(--text);font-weight:600}

.cat-val{font-size:13px;color:var(--text2);padding:0 14px;display:flex;align-items:center;height:100%;cursor:text;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;transition:0.1s}
.cat-val:hover{background:rgba(255,255,255,0.03);color:var(--text)}
.cat-sel{position:absolute;inset:0;border:none;outline:none;box-shadow:inset 0 0 0 2px var(--accent);background:#14161d;font-size:13px;font-family:var(--f);color:var(--text);padding:0 14px;z-index:20;cursor:pointer}

.tech-wrap{display:flex;align-items:center;gap:6px;padding:0 12px;height:100%;overflow:hidden;cursor:pointer;flex-wrap:nowrap}
.pill{display:inline-flex;align-items:center;font-size:10.5px;font-weight:600;padding:2px 8px;border-radius:6px;border:1px solid;white-space:nowrap;font-family:var(--mono);flex-shrink:0;background:rgba(255,255,255,0.05)}
.pill-more{font-size:11px;color:var(--text2);font-family:var(--mono);flex-shrink:0;background:rgba(255,255,255,0.05);padding:2px 6px;border-radius:6px}
.tech-pop{
  position:absolute;top:calc(100% + 6px);left:12px;
  background:#14161d;border:1px solid var(--line2);border-radius:12px;
  box-shadow:var(--shadow-pop);z-index:500;padding:14px;min-width:260px;animation:fadeIn 0.1s ease-out;
}
.tp-tags{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;min-height:28px}
.tp-tag{display:inline-flex;align-items:center;gap:4px;font-size:11.5px;font-weight:600;padding:3px 8px;border-radius:6px;border:1px solid;font-family:var(--mono)}
.tp-rm{background:none;border:none;cursor:pointer;font-size:14px;opacity:0.5;color:inherit;padding:0;line-height:1;transition:0.1s}
.tp-rm:hover{opacity:1;transform:scale(1.1)}
.tp-inp{width:100%;height:36px;padding:0 12px;border:1px solid var(--line2);border-radius:8px;font-size:13px;font-family:var(--mono);outline:none;background:rgba(0,0,0,0.2);color:var(--text);transition:0.15s}
.tp-inp:focus{border-color:var(--accent);background:#14161d;box-shadow:0 0 0 2px var(--accent-bg)}
.tp-hint{font-size:11px;color:var(--text3);margin-top:8px;text-align:center}

.pri-wrap{display:flex;align-items:center;justify-content:center;gap:3px;height:100%;padding:0 8px;cursor:pointer}
.pstar{font-size:16px;line-height:1;color:var(--line2);transition:color 0.1s, transform 0.1s;user-select:none}
.pstar.on{color:#f59e0b;text-shadow:0 0 8px rgba(245,158,11,0.4)}
.pri-wrap:hover .pstar{color:#fbbf24}
.pri-wrap:hover .pstar:hover{transform:scale(1.2)}
.pri-wrap:hover .pstar.on{color:#f59e0b}

.time-wrap{display:flex;align-items:center;gap:6px;padding:0 10px;height:100%}
.time-v{font-size:13px;font-family:var(--mono);color:var(--text);font-weight:500}
.time-u{font-size:11.5px;color:var(--text3)}
.time-add{
  width:22px;height:22px;border-radius:6px;border:1px solid var(--line2);
  background:rgba(255,255,255,0.05);cursor:pointer;font-size:16px;line-height:1;
  display:none;align-items:center;justify-content:center;color:var(--text2);
  transition:0.15s;flex-shrink:0;padding:0;
}
.time-add:hover{background:var(--accent-bg);color:var(--accent);border-color:var(--accent)}
tbody tr:hover .time-add{display:flex}
.time-pop{
  position:absolute;top:calc(100% + 6px);right:0;
  background:#14161d;border:1px solid var(--line2);border-radius:12px;
  box-shadow:var(--shadow-pop);z-index:500;padding:16px;width:240px;animation:fadeIn 0.1s ease-out;
}
.tp-title{font-size:11.5px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:0.06em;margin-bottom:12px}
.tp-row{display:flex;gap:8px;align-items:center}
.tp-inp-h{flex:1;height:38px;padding:0 12px;border:1px solid var(--line2);border-radius:8px;font-size:15px;font-family:var(--mono);outline:none;background:rgba(0,0,0,0.2);color:var(--text);width:0}
.tp-inp-h:focus{border-color:var(--accent);background:#14161d;box-shadow:0 0 0 2px var(--accent-bg)}
.tp-log-btn{height:38px;padding:0 16px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap;flex-shrink:0;transition:0.1s}
.tp-log-btn:hover{background:#0ea5e9;box-shadow:0 0 10px var(--accent-bg)}
.tp-presets{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}
.tp-preset{font-size:12px;padding:6px 12px;border-radius:6px;border:1px solid var(--line2);background:rgba(255,255,255,0.03);color:var(--text2);cursor:pointer;font-family:var(--mono);transition:0.15s}
.tp-preset:hover{background:rgba(255,255,255,0.08);color:var(--text);border-color:var(--text3)}

.dc{font-size:12px;font-family:var(--mono);color:var(--text3);padding:0 14px;display:flex;align-items:center;height:100%;gap:6px}
.stale-dot{font-size:8px;transition:0.1s;text-shadow:0 0 4px currentColor}

.links-wrap{display:flex;align-items:center;gap:8px;padding:0 14px;height:100%;overflow:hidden}
.lnk{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:600;color:var(--accent);text-decoration:none;padding:3px 10px;border-radius:6px;background:var(--accent-bg);border:1px solid rgba(56,189,248,0.2);transition:0.15s;white-space:nowrap}
.lnk:hover{background:rgba(56,189,248,0.25);box-shadow:0 0 8px var(--accent-bg)}
.lnk-ghost{font-size:12.5px;color:var(--text3);cursor:pointer;transition:0.1s;flex-shrink:0}
.lnk-ghost:hover{color:var(--text)}

.notes-wrap{display:flex;align-items:center;padding:0 14px;height:100%;gap:8px}
.notes-lnk{display:inline-flex;align-items:center;gap:4px;font-size:12.5px;color:var(--text);text-decoration:none;padding:3px 10px;border-radius:6px;border:1px solid var(--line2);background:rgba(255,255,255,0.03);transition:0.15s;white-space:nowrap}
.notes-lnk:hover{background:rgba(255,255,255,0.08);border-color:var(--text3)}
.notes-ghost{font-size:12.5px;color:var(--text3);cursor:pointer;transition:0.1s}
.notes-ghost:hover{color:var(--text)}

.act-wrap{display:flex;align-items:center;justify-content:center;gap:5px;height:100%;opacity:0;transition:0.15s}
tbody tr:hover .act-wrap{opacity:1}
.act-b{width:26px;height:26px;border-radius:6px;border:1px solid var(--line2);background:rgba(255,255,255,0.03);cursor:pointer;font-size:14px;display:flex;align-items:center;justify-content:center;color:var(--text2);transition:0.15s}
.act-b:hover{background:rgba(255,255,255,0.1);color:var(--text)}
.act-b.dup:hover{background:rgba(16,185,129,0.15);border-color:#10b981;color:#10b981;box-shadow:0 0 8px rgba(16,185,129,0.2)}
.act-b.del:hover{background:rgba(239,68,68,0.15);border-color:#ef4444;color:#ef4444;box-shadow:0 0 8px rgba(239,68,68,0.2)}
.act-b.exp:hover{background:var(--accent-bg);border-color:var(--accent);color:var(--accent)}

/* ═══════════════════════════════════════════════
   EXPAND PANEL
═══════════════════════════════════════════════ */
tr.expand-row td{padding:0;height:auto;background:var(--bg2)!important;border-bottom:1px solid var(--line)!important;box-shadow:inset 0 4px 6px rgba(0,0,0,0.2)}
.expand-panel{padding:20px 24px 20px 62px;display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px 32px}
.ep-field{display:flex;flex-direction:column;gap:6px}
.ep-label{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.06em}
.ep-val{font-size:13px;color:var(--text2);line-height:1.6}
.ep-val a{color:var(--accent);text-decoration:none}
.ep-val a:hover{text-decoration:underline;text-underline-offset:2px}
.ep-edit{
  width:100%;border:none;outline:none;background:transparent;
  font-size:13px;color:var(--text);font-family:var(--f);
  border-bottom:1px solid var(--line2);padding-bottom:4px;transition:0.15s;
}
.ep-edit:focus{border-color:var(--accent);box-shadow:0 1px 0 var(--accent)}
.ep-tags-full{display:flex;flex-wrap:wrap;gap:6px}

/* ═══════════════════════════════════════════════
   MOBILE
═══════════════════════════════════════════════ */
@media(max-width:768px){
  .tbl-outer{display:none}
  .mobile-list{display:flex;flex-direction:column;flex:1;overflow-y:auto;padding:12px}
}
@media(min-width:769px){.mobile-list{display:none}}
.m-card{background:rgba(255,255,255,0.02);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:12px;transition:box-shadow 0.15s}
.m-card:hover{box-shadow:var(--shadow-row);background:rgba(255,255,255,0.04);border-color:var(--line2)}
.m-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:10px;margin-bottom:10px}
.m-name{font-size:15px;font-weight:700;color:var(--text);flex:1;line-height:1.3}
.m-desc{font-size:12.5px;color:var(--text2);margin-top:4px}
.m-row{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:10px}
.m-tags{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}
.m-stat{font-size:12px;color:var(--text2);display:flex;align-items:center;gap:4px;background:rgba(255,255,255,0.03);padding:2px 8px;border-radius:6px}
.m-links{display:flex;gap:10px;margin-top:12px}
.m-edit-btn{font-size:12px;color:var(--accent);cursor:pointer;margin-top:10px;display:inline-block;padding:4px 10px;border-radius:6px;background:var(--accent-bg)}

/* ═══════════════════════════════════════════════
   MOBILE SHEET
═══════════════════════════════════════════════ */
.sheet-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.6);backdrop-filter:blur(10px);z-index:400;display:flex;flex-direction:column;justify-content:flex-end;opacity:0;pointer-events:none;transition:opacity 0.2s}
.sheet-overlay.open{opacity:1;pointer-events:auto}
.sheet{background:#11131a;border-radius:20px 20px 0 0;max-height:90vh;overflow-y:auto;padding:0 24px 32px;transform:translateY(100%);transition:transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);border-top:1px solid var(--line2)}
.sheet-overlay.open .sheet{transform:translateY(0)}
.sheet-handle{width:40px;height:5px;background:var(--line2);border-radius:3px;margin:12px auto 20px}
.sheet-title{font-size:18px;font-weight:800;margin-bottom:20px;color:var(--text)}
.sf{display:flex;flex-direction:column;gap:16px}
.sf-group{display:flex;flex-direction:column;gap:6px}
.sf-label{font-size:11.5px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:0.06em}
.sf-inp, .sf-sel{height:44px;padding:0 14px;border:1px solid var(--line2);border-radius:8px;font-size:14.5px;font-family:var(--f);color:var(--text);background:rgba(0,0,0,0.3);outline:none;width:100%}
.sf-inp:focus, .sf-sel:focus{border-color:var(--accent);background:rgba(255,255,255,0.02);box-shadow:0 0 0 3px var(--accent-bg)}
.sheet-ft{display:flex;gap:12px;margin-top:24px}
.sheet-save{flex:1;height:48px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:15px;font-weight:700;cursor:pointer}
.sheet-cancel{height:48px;padding:0 24px;border:1px solid var(--line2);border-radius:8px;background:transparent;color:var(--text2);font-size:15px;font-weight:600;cursor:pointer}

/* ═══════════════════════════════════════════════
   LOGIN
═══════════════════════════════════════════════ */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,0.6);backdrop-filter:blur(12px);z-index:600;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.2s}
.overlay.open{opacity:1;pointer-events:auto}
.login-box{background:#11131a;border-radius:20px;box-shadow:0 24px 64px rgba(0,0,0,0.6);width:320px;padding:32px;border:1px solid var(--line2);text-align:center;transform:translateY(16px);transition:transform 0.2s cubic-bezier(0.4, 0, 0.2, 1)}
.overlay.open .login-box{transform:translateY(0)}
.lb-ico{font-size:32px;margin-bottom:12px;filter:drop-shadow(0 4px 12px rgba(255,255,255,0.1))}
.lb-h{font-size:18px;font-weight:800;letter-spacing:-.01em;margin-bottom:6px;color:var(--text)}
.lb-s{font-size:13px;color:var(--text2);margin-bottom:24px}
.lb-inp{width:100%;height:44px;padding:0 16px;border:1px solid var(--line2);border-radius:8px;font-size:15px;outline:none;background:rgba(0,0,0,0.3);color:var(--text);letter-spacing:0.15em;margin-bottom:12px;transition:0.15s;text-align:center}
.lb-inp:focus{border-color:var(--accent);background:rgba(255,255,255,0.02);box-shadow:0 0 0 3px var(--accent-bg)}
.lb-err{font-size:12.5px;color:#ef4444;min-height:18px;margin-bottom:12px}
.lb-btn{width:100%;height:44px;border:none;border-radius:8px;background:var(--accent);color:#fff;font-size:14.5px;font-weight:700;cursor:pointer;transition:0.15s;box-shadow:0 4px 12px var(--accent-bg)}
.lb-btn:hover{background:#0ea5e9;transform:translateY(-1px)}

/* ═══════════════════════════════════════════════
   CMD PALETTE
═══════════════════════════════════════════════ */
.cmd-bg{position:fixed;inset:0;background:rgba(0,0,0,0.4);backdrop-filter:blur(8px);z-index:700;display:flex;align-items:flex-start;justify-content:center;padding-top:12vh;opacity:0;pointer-events:none;transition:opacity 0.15s}
.cmd-bg.open{opacity:1;pointer-events:auto}
.cmd-box{background:#14161d;border-radius:16px;box-shadow:0 24px 64px rgba(0,0,0,0.5);width:500px;border:1px solid var(--line2);overflow:hidden;transform:translateY(-10px) scale(0.98);transition:all 0.15s cubic-bezier(0.4, 0, 0.2, 1)}
.cmd-bg.open .cmd-box{transform:translateY(0) scale(1)}
.cmd-inp{width:100%;height:56px;padding:0 20px;border:none;border-bottom:1px solid var(--line);outline:none;font-size:16px;color:var(--text);background:transparent}
.cmd-list{max-height:340px;overflow-y:auto;padding:8px}
.ci{display:flex;align-items:center;gap:12px;padding:12px 14px;border-radius:10px;cursor:pointer;font-size:13.5px;color:var(--text2);transition:0.1s}
.ci:hover,.ci.sel{background:rgba(255,255,255,0.06);color:var(--text)}
.ci-ico{font-size:16px;width:24px;text-align:center;flex-shrink:0}
.ci-lbl{flex:1;font-weight:500}
.ci-hint{font-size:11px;color:var(--text3);font-family:var(--mono)}
.cmd-ft{padding:10px 16px;border-top:1px solid var(--line);background:rgba(0,0,0,0.2);display:flex;gap:16px}
.ck{font-size:11px;color:var(--text3);display:flex;align-items:center;gap:6px}
.kbd{font-family:var(--mono);background:rgba(255,255,255,0.05);border:1px solid var(--line2);border-radius:4px;padding:2px 6px;font-size:10px;color:var(--text2)}

/* ═══════════════════════════════════════════════
   TOASTS & ANIMATIONS
═══════════════════════════════════════════════ */
.toasts{position:fixed;bottom:24px;right:24px;z-index:800;display:flex;flex-direction:column;gap:10px;pointer-events:none}
.toast{background:#1e293b;color:#fff;border-radius:10px;padding:12px 20px;font-size:13.5px;font-weight:600;box-shadow:0 8px 32px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.1);animation:tIn 0.25s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;display:flex;align-items:center;gap:8px}
.toast.out{animation:tOut 0.2s ease forwards}
@keyframes tIn{from{opacity:0;transform:translateY(20px) scale(0.95)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes tOut{to{opacity:0;transform:translateY(10px) scale(0.95)}}
@keyframes fadeIn{from{opacity:0;transform:translateY(-4px)}to{opacity:1;transform:translateY(0)}}
</style>"""

# Replace CSS
html = re.sub(r'<style>.*?</style>', NEW_CSS, html, flags=re.DOTALL)

# 2. Fix JS bugs
js_delete = """async function deleteRow(id){
  if(!isAdmin) return;
  if(!confirm('Delete this project?')) return;"""

html = re.sub(r"async function deleteRow\(id\)\{\s*if\(!confirm\('Delete this project\?'\)\) return;", js_delete, html)

js_dup = """async function duplicateRow(id){
  if(!isAdmin) return;"""

html = re.sub(r"async function duplicateRow\(id\)\{\s*if\(!isAdmin\) return;", js_dup, html)

js_row = """<div class="act-wrap">
        <button class="act-b exp" onclick="toggleExpand(${p.id})" title="${expanded?'Collapse':'Expand'}">⌄</button>
        ${isAdmin ? `<button class="act-b dup" onclick="duplicateRow(${p.id})" title="Duplicate">⎘</button>
        <button class="act-b del" onclick="deleteRow(${p.id})"    title="Delete">✕</button>` : ''}
      </div>"""

html = re.sub(r'<div class="act-wrap\$\{.*?\}.*?</div>', js_row, html, flags=re.DOTALL)

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("done")
