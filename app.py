from flask import Flask, request, jsonify, render_template
import sqlite3
from flask_cors import CORS
from datetime import datetime
import os

DB = os.path.join(os.path.dirname(__file__), "assignments.db")


def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        status TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()


app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

ensure_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/assignments", methods=["GET", "POST"])
def assignments():
    if request.method == "GET":
        conn = get_db()
        cur = conn.execute(
            "SELECT * FROM assignments ORDER BY due_date IS NULL, due_date"
        )
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return jsonify(rows)

    data = request.get_json() or {}
    title = data.get("title", "")
    description = data.get("description", "")
    due_date = data.get("due_date")
    status = data.get("status", "pending")

    conn = get_db()
    cur = conn.execute(
        "INSERT INTO assignments (title, description, due_date, status, created_at) VALUES (?,?,?,?,?)",
        (title, description, due_date, status, datetime.utcnow().isoformat()),
    )
    conn.commit()
    aid = cur.lastrowid
    conn.close()
    return jsonify({"id": aid}), 201


@app.route("/api/assignments/<int:aid>", methods=["PUT", "DELETE"])
def assignment_detail(aid):
    conn = get_db()
    if request.method == "PUT":
        data = request.get_json() or {}
        fields = []
        vals = []
        for k in ("title", "description", "due_date", "status"):
            if k in data:
                fields.append(f"{k}=?")
                vals.append(data[k])
        if fields:
            vals.append(aid)
            conn.execute(f"UPDATE assignments SET {', '.join(fields)} WHERE id=?", vals)
            conn.commit()
        conn.close()
        return jsonify({"ok": True})

    conn.execute("DELETE FROM assignments WHERE id=?", (aid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(debug=True)
