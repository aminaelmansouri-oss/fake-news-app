import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "history.db"


def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database schema."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_type TEXT NOT NULL,
            source TEXT,
            text_preview TEXT,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            fake_score REAL NOT NULL,
            real_score REAL NOT NULL,
            word_count INTEGER,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_analysis(data: dict) -> int:
    """Save an analysis result to DB. Returns the new record ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO analyses
            (input_type, source, text_preview, prediction, confidence,
             fake_score, real_score, word_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("input_type", "text"),
        data.get("source", ""),
        data.get("text_preview", "")[:200],
        data.get("prediction", ""),
        data.get("confidence", 0.0),
        data.get("fake_score", 0.0),
        data.get("real_score", 0.0),
        data.get("word_count", 0),
        datetime.now().isoformat()
    ))
    conn.commit()
    record_id = cursor.lastrowid
    conn.close()
    return record_id


def get_history(limit: int = 50) -> list:
    """Retrieve analysis history."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM analyses ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows


def get_stats() -> dict:
    """Retrieve aggregate statistics."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM analyses")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as cnt FROM analyses WHERE prediction='FAKE'")
    fake_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM analyses WHERE prediction='REAL'")
    real_count = cursor.fetchone()["cnt"]

    cursor.execute("SELECT AVG(confidence) as avg_conf FROM analyses")
    avg_conf = cursor.fetchone()["avg_conf"] or 0.0

    # Last 7 days distribution
    cursor.execute("""
        SELECT DATE(created_at) as day, prediction, COUNT(*) as cnt
        FROM analyses
        WHERE created_at >= DATE('now', '-7 days')
        GROUP BY day, prediction
        ORDER BY day ASC
    """)
    daily = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return {
        "total": total,
        "fake_count": fake_count,
        "real_count": real_count,
        "fake_ratio": round(fake_count / total * 100, 1) if total > 0 else 0,
        "real_ratio": round(real_count / total * 100, 1) if total > 0 else 0,
        "avg_confidence": round(avg_conf * 100, 1),
        "daily": daily
    }


# Initialize on import
init_db()
