from flask import Flask, request, render_template
import datetime, os

app = Flask(__name__)

LOG_PATH = os.path.join("logs", "scammer.txt")

def log_visit(notes=""):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = request.remote_addr
    ua = request.headers.get("User-Agent")
    ref = request.headers.get("Referer")
    lang = request.headers.get("Accept-Language")
    method = request.method
    path = request.path
    query = request.query_string.decode("utf-8", errors="ignore")

    log_line = (
        f"{ts} | IP:{ip} | Method:{method} | Path:{path}?{query} | "
        f"UA:{ua} | Ref:{ref} | Lang:{lang} | Notes:{notes}"
    )

    os.makedirs("logs", exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

@app.route("/")
def home():
    log_visit(notes="home")
    return "<h1>Welcome to the Anti-Scam Training Hub</h1><p>This site logs visits for educational purposes.</p>"

@app.route("/bait")
def bait():
    log_visit(notes="bait")
    return "<h1 style='color:red;'>YOU GOT HACKED</h1><p>This is a training simulation.</p>"
@app.route("/dashboard")
def dashboard():
    logs = []
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f.readlines()[-50:]:  # show last 50 entries
                parts = line.strip().split(" | ")
                logs.append(parts)
    except FileNotFoundError:
        logs = []

    return render_template("dashboard.html", logs=logs, title="Dashboard")

if __name__ == "__main__":
    app.run(debug=True)

