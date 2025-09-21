import json, os, subprocess
from pathlib import Path
from flask import Flask, request, redirect, url_for, render_template, flash

APP_FILE = Path("apps.json")
PROCS = {}

app = Flask(__name__)
app.secret_key = "dev-key"  # change in production

class AppItem(dict):
    __getattr__ = dict.get
    def __setattr__(self, k, v): self[k] = v

def load_apps():
    if APP_FILE.exists():
        data = json.loads(APP_FILE.read_text(encoding="utf-8"))
    else:
        data = []
    for i, a in enumerate(data):
        a.setdefault("id", str(i+1))
    APP_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return [AppItem(a) for a in data]

def save_apps(items):
    APP_FILE.write_text(json.dumps(items, indent=2), encoding="utf-8")

def creationflags():
    return 0

@app.route("/")
def index():
    apps = load_apps()
    return render_template("index.html", apps=apps, procs=PROCS)

@app.post("/add")
def add_app():
    name = request.form["name"].strip()
    cwd = request.form["cwd"].strip()
    cmd = request.form["cmd"].strip()
    apps = load_apps()
    new_id = str(max([int(a["id"]) for a in apps], default=0) + 1)
    apps.append({"id": new_id, "name": name, "cwd": cwd, "cmd": cmd})
    save_apps(apps)
    flash(f"Added: {name}")
    return redirect(url_for("index"))

@app.post("/start/<app_id>")
def start_app(app_id):
    if app_id in PROCS and PROCS[app_id].poll() is None:
        flash("Already running")
        return redirect(url_for("index"))
    apps = load_apps()
    item = next((a for a in apps if a.id == app_id), None)
    if not item:
        flash("Not found")
        return redirect(url_for("index"))
    if not os.path.isdir(item.cwd):
        flash("Working dir not found")
        return redirect(url_for("index"))
    p = subprocess.Popen(item.cmd, cwd=item.cwd, shell=True, creationflags=creationflags())
    PROCS[app_id] = p
    flash(f"Started {item.name} (PID {p.pid})")
    return redirect(url_for("index"))

@app.post("/stop/<app_id>")
def stop_app(app_id):
    p = PROCS.get(app_id)
    if not p or p.poll() is not None:
        PROCS.pop(app_id, None)
        flash("Not running")
        return redirect(url_for("index"))
    try:
        p.terminate()
    finally:
        PROCS.pop(app_id, None)
    flash("Stopped")
    return redirect(url_for("index"))

@app.post("/delete/<app_id>")
def delete_app(app_id):
    apps = load_apps()
    apps = [a for a in apps if a["id"] != app_id]
    save_apps(apps)
    PROCS.pop(app_id, None)
    flash("Deleted")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=False)
