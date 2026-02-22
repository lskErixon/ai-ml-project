import os
import sys
import subprocess
import json
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

PID_FILE = "logs/collector.pid"
OUT_LOG = "logs/collector.out.log"
ERR_LOG = "logs/collector.err.log"

os.makedirs("logs", exist_ok=True)


def _is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def _count_jsonl_rows(path: str) -> int:
    if not os.path.exists(path):
        return 0
    with open(path, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)

@app.get("/admin")
def admin():
    cfg = json.loads(Path("config/config.json").read_text(encoding="utf-8"))
    dataset_path = cfg["dataset_path"]
    rows = _count_jsonl_rows(dataset_path)
    default_names = ", ".join(cfg.get("default_names", []))
    return render_template("admin.html", rows=rows, default_names=default_names)

@app.post("/admin/start")
def admin_start():
    minutes = int(request.form.get("minutes", "10"))
    seconds = minutes * 60

    stop_name = (request.form.get("stop_name") or "").strip()

    if os.path.exists(PID_FILE):
        try:
            pid = int(Path(PID_FILE).read_text(encoding="utf-8").strip())
            if _is_running(pid):
                return redirect(url_for("admin"))
        except Exception:
            pass

    cmd = [sys.executable, "app/collector/run_collector.py", str(seconds)]
    if stop_name:
        cmd += ["--names", stop_name]

    p = subprocess.Popen(
        cmd,
        stdout=open(OUT_LOG, "a", encoding="utf-8"),
        stderr=open(ERR_LOG, "a", encoding="utf-8"),
    )
    Path(PID_FILE).write_text(str(p.pid), encoding="utf-8")
    return redirect(url_for("admin"))


@app.get("/admin/status")
def admin_status():
    if not os.path.exists(PID_FILE):
        return jsonify({"running": False})
    try:
        pid = int(Path(PID_FILE).read_text(encoding="utf-8").strip())
    except Exception:
        return jsonify({"running": False})

    running = _is_running(pid)
    return jsonify({"running": running, "pid": pid})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

