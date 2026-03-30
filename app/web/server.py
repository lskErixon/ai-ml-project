import os
import sys
import json
import pickle
import subprocess
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from sklearn.metrics import mean_absolute_error, mean_squared_error


app = Flask(__name__)

MODEL_PATH = "models/delay_model.pkl"
CONFIG_PATH = "config/config.json"
DATASET_PATH = "data/dataset/departures.jsonl"
FEATURES_PATH = "data/processed/features.csv"
PID_FILE = "logs/collector.pid"

os.makedirs("logs", exist_ok=True)


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def load_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


def count_dataset_rows():
    if not os.path.exists(DATASET_PATH):
        return 0
    with open(DATASET_PATH, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def is_process_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def encode_stop(stop_name: str) -> int:
    mapping = {
        "Karlovo náměstí": 0,
        "I. P. Pavlova": 1,
        "Anděl": 2
    }
    return mapping.get(stop_name, 0)


def encode_platform(platform: str) -> int:
    mapping = {
        "A": 0,
        "B": 1,
        "C": 2
    }
    return mapping.get(platform, 0)


def encode_headsign(headsign: str) -> int:
    mapping = {
        "Nádraží Braník": 0,
        "Spojovací": 1,
        "Bílá Hora": 2,
        "Řepy": 3
    }
    return mapping.get(headsign, 0)


def get_model_metrics():
    if not os.path.exists(FEATURES_PATH) or not os.path.exists(MODEL_PATH):
        return None, None

    df = pd.read_csv(FEATURES_PATH)
    model = load_model()

    X = df.drop(columns=["delay_min"])
    y = df["delay_min"]
    y_pred = model.predict(X)

    mae = round(mean_absolute_error(y, y_pred), 4)
    mse = round(mean_squared_error(y, y_pred), 4)

    return mae, mse


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    mae, mse = get_model_metrics()

    if request.method == "POST":
        stop_name = request.form.get("stop_name", "").strip()
        route_num = request.form.get("route_num", "").strip()
        platform = request.form.get("platform", "").strip()
        headsign = request.form.get("headsign", "").strip()
        hour = request.form.get("hour", "").strip()
        minute = request.form.get("minute", "").strip()
        day_of_week = request.form.get("day_of_week", "").strip()

        try:
            features = {
                "hour": int(hour),
                "minute": int(minute),
                "day_of_week": int(day_of_week),
                "is_weekend": 1 if int(day_of_week) in [5, 6] else 0,
                "is_peak": 1 if int(hour) in [7, 8, 15, 16, 17] else 0,
                "stop_encoded": encode_stop(stop_name),
                "platform_encoded": encode_platform(platform),
                "route_num": int(route_num),
                "headsign_encoded": encode_headsign(headsign),
            }

            model = load_model()
            df = pd.DataFrame([features])
            pred = model.predict(df)[0]
            prediction = round(pred, 2)

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction, mae=mae, mse=mse)


@app.route("/admin", methods=["GET"])
def admin():
    cfg = load_config()
    rows = count_dataset_rows()
    default_names = ", ".join(cfg.get("default_names", []))

    running = False
    pid = None

    if os.path.exists(PID_FILE):
        try:
            pid = int(Path(PID_FILE).read_text(encoding="utf-8").strip())
            running = is_process_running(pid)
        except Exception:
            running = False

    return render_template(
        "admin.html",
        rows=rows,
        default_names=default_names,
        running=running,
        pid=pid
    )


@app.route("/admin/start", methods=["POST"])
def admin_start():
    minutes = int(request.form.get("minutes", "10"))
    seconds = minutes * 60

    stop_name = request.form.get("stop_name", "").strip()

    cmd = [sys.executable, "app/collector/run_collector.py", str(seconds)]
    if stop_name:
        cmd += ["--names", stop_name]

    p = subprocess.Popen(
        cmd,
        stdout=open("logs/collector.out.log", "a", encoding="utf-8"),
        stderr=open("logs/collector.err.log", "a", encoding="utf-8"),
    )

    Path(PID_FILE).write_text(str(p.pid), encoding="utf-8")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)