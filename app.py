from flask import Flask, render_template, request, jsonify
import sqlite3, os

app = Flask(__name__)
DB = os.environ.get("EVENTS_DB", os.path.join(os.path.dirname(__file__), "data/n5lcc.db"))

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DB), exist_ok=True)  # ensure /data exists
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id    INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                start TEXT NOT NULL,
                end   TEXT,
                color TEXT DEFAULT '#3788d8'
            )
        """)
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/events", methods=["GET"])
def get_events():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM events ORDER BY start").fetchall()
    return jsonify([dict(r) for r in rows])

@app.route("/api/events", methods=["POST"])
def create_event():
    data  = request.get_json()
    title = data.get("title","").strip()
    start = data.get("start","").strip()
    end   = data.get("end","").strip() or None
    color = data.get("color","#3788d8")
    if not title or not start:
        return jsonify({"error": "Title and start are required"}), 400
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO events (title,start,end,color) VALUES (?,?,?,?)",
            (title, start, end, color))
        conn.commit()
    return jsonify({"id": cur.lastrowid, "title": title,
                    "start": start, "end": end, "color": color}), 201

@app.route("/api/events/<int:event_id>", methods=["PUT"])
def update_event(event_id):
    data  = request.get_json()
    title = data.get("title", "").strip()
    start = data.get("start", "").strip()
    end   = data.get("end",   "").strip() or None
    color = data.get("color", "#3788d8")
    if not title or not start:
        return jsonify({"error": "Title and start are required"}), 400
    with get_db() as conn:
        conn.execute(
            "UPDATE events SET title=?, start=?, end=?, color=? WHERE id=?",
            (title, start, end, color, event_id)
        )
        conn.commit()
    return jsonify({"ok": True})

@app.route("/api/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    with get_db() as conn:
        conn.execute("DELETE FROM events WHERE id=?", (event_id,))
        conn.commit()
    return jsonify({"ok": True})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=False, host="0.0.0.0", port=port)