from flask import Flask, request, jsonify, session, render_template, make_response
from flask_cors import CORS
import json, os, datetime, csv, io
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "devden-final-secret")
CORS(app, supports_credentials=True)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ganesh123")
DATA_FILE      = "projects.json"
BACKUP_DIR     = "backups"

os.makedirs(BACKUP_DIR, exist_ok=True)

# ── logging setup ─────────────────────────────────────────
os.makedirs("logs", exist_ok=True)
handler = RotatingFileHandler("logs/app.log", maxBytes=100000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

# ── error handlers ────────────────────────────────────────
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Not found"}), 404
    return render_template("index.html"), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Server Error: {error}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500

# ── helpers ───────────────────────────────────────────────
def load():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE) as f: return json.load(f)

def save(data):
    tmp = DATA_FILE + ".tmp"
    with open(tmp, "w") as f: json.dump(data, f, indent=2)
    os.replace(tmp, DATA_FILE)
    _auto_backup(data)

def _auto_backup(data):
    today_str = datetime.date.today().isoformat()
    path = os.path.join(BACKUP_DIR, f"projects_{today_str}.json")
    with open(path, "w") as f: json.dump(data, f, indent=2)
    backups = sorted(os.listdir(BACKUP_DIR))
    for old in backups[:-30]:
        try: os.remove(os.path.join(BACKUP_DIR, old))
        except: pass

def is_admin(): return session.get("admin") is True
def today(): return datetime.date.today().isoformat()

# ── auth ──────────────────────────────────────────────────
@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/login", methods=["POST"])
def login():
    if request.json.get("password") == ADMIN_PASSWORD:
        session["admin"] = True
        return jsonify({"ok": True})
    return jsonify({"ok": False}), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("admin", None)
    return jsonify({"ok": True})

@app.route("/api/me")
def me(): return jsonify({"admin": is_admin()})

# ── projects ──────────────────────────────────────────────
@app.route("/api/projects", methods=["GET"])
def get_projects(): return jsonify(load())

@app.route("/api/projects", methods=["POST"])
def add_project():
    if not is_admin(): return jsonify({"error": "Unauthorized"}), 403
    projects = load()
    p = request.json or {}
    p["id"]          = int(datetime.datetime.now().timestamp() * 1000)
    p["createdAt"]   = today()
    p["updatedAt"]   = today()
    p["workedAt"]    = today()
    p["totalTime"]   = float(p.get("totalTime") or 0)
    p.setdefault("tech",        [])
    p.setdefault("flagship",    False)
    p.setdefault("description", "")
    p.setdefault("notes",       "")
    p.setdefault("status",      "Idea")
    p.setdefault("priority",    0)
    p.setdefault("order",       len(projects))
    p.setdefault("name",        "")
    p.setdefault("category",    "")
    p.setdefault("github",      "")
    p.setdefault("demo",        "")
    projects.append(p)
    save(projects)
    return jsonify(p), 201

# ── IMPORTANT: reorder must be BEFORE /<int:pid> ─────────
@app.route("/api/projects/reorder", methods=["POST"])
def reorder():
    if not is_admin(): return jsonify({"error": "Unauthorized"}), 403
    order = request.json.get("order", [])
    projects = load()
    id_map = {p["id"]: p for p in projects}
    reordered = []
    for idx, pid in enumerate(order):
        if pid in id_map:
            id_map[pid]["order"] = idx
            reordered.append(id_map[pid])
    seen = set(order)
    for p in projects:
        if p["id"] not in seen:
            reordered.append(p)
    save(reordered)
    return jsonify({"ok": True})

@app.route("/api/projects/<int:pid>", methods=["PUT"])
def update_project(pid):
    if not is_admin(): return jsonify({"error": "Unauthorized"}), 403
    projects = load()
    for i, p in enumerate(projects):
        if p["id"] == pid:
            data = request.json or {}
            updated = {**p, **data, "id": pid}
            updated["updatedAt"] = today()
            projects[i] = updated
            save(projects)
            return jsonify(updated)
    return jsonify({"error": "Not found"}), 404

@app.route("/api/projects/<int:pid>", methods=["DELETE"])
def delete_project(pid):
    if not is_admin(): return jsonify({"error": "Unauthorized"}), 403
    save([p for p in load() if p["id"] != pid])
    return jsonify({"ok": True})

@app.route("/api/projects/<int:pid>/log-time", methods=["POST"])
def log_time(pid):
    if not is_admin(): return jsonify({"error": "Unauthorized"}), 403
    hours = float(request.json.get("hours", 0))
    if hours <= 0: return jsonify({"error": "Hours must be positive"}), 400
    projects = load()
    for i, p in enumerate(projects):
        if p["id"] == pid:
            p["totalTime"] = round(float(p.get("totalTime") or 0) + hours, 1)
            p["workedAt"]  = today()
            p["updatedAt"] = today()
            projects[i] = p
            save(projects)
            return jsonify(p)
    return jsonify({"error": "Not found"}), 404

# ── export ────────────────────────────────────────────────
@app.route("/api/export/json")
def export_json():
    data = json.dumps(load(), indent=2)
    r = make_response(data)
    r.headers["Content-Type"] = "application/json"
    r.headers["Content-Disposition"] = f'attachment; filename="devden_{today()}.json"'
    return r

@app.route("/api/export/csv")
def export_csv():
    projects = load()
    fields = ["id","name","description","status","category","tech","priority",
              "totalTime","workedAt","updatedAt","createdAt","github","demo","notes","flagship"]
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    for p in projects:
        row = {**p}
        row["tech"] = ", ".join(p.get("tech") or [])
        w.writerow(row)
    r = make_response(buf.getvalue())
    r.headers["Content-Type"] = "text/csv"
    r.headers["Content-Disposition"] = f'attachment; filename="devden_{today()}.csv"'
    return r

if __name__ == "__main__":
    app.logger.info("Starting development server...")
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))