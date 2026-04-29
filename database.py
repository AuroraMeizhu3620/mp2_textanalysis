import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "articles.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS saved_articles (
                id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                title              TEXT    NOT NULL,
                source             TEXT,
                tags               TEXT    DEFAULT '[]',
                ai_analysis        TEXT,
                sentiment_compound REAL,
                sentiment_label    TEXT,
                framing_ratio      REAL,
                created_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_article(title, source, tags, ai_analysis, sentiment_compound, sentiment_label, framing_ratio):
    with _connect() as conn:
        conn.execute(
            """INSERT INTO saved_articles
               (title, source, tags, ai_analysis, sentiment_compound, sentiment_label, framing_ratio)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                title,
                source,
                json.dumps([t.lower().strip() for t in tags if t.strip()]),
                json.dumps(ai_analysis) if ai_analysis else None,
                float(sentiment_compound),
                sentiment_label,
                float(framing_ratio),
            ),
        )
        conn.commit()


def all_tags():
    """Return [(tag, count)] sorted by count descending."""
    counts = {}
    with _connect() as conn:
        for row in conn.execute("SELECT tags FROM saved_articles").fetchall():
            for tag in json.loads(row["tags"] or "[]"):
                t = tag.lower().strip()
                if t:
                    counts[t] = counts.get(t, 0) + 1
    return sorted(counts.items(), key=lambda x: -x[1])


def articles_by_tag(tag):
    """Return all article dicts that carry the given tag, newest first."""
    tag_lower = tag.lower().strip()
    results = []
    with _connect() as conn:
        for row in conn.execute(
            "SELECT * FROM saved_articles ORDER BY created_at DESC"
        ).fetchall():
            tags = json.loads(row["tags"] or "[]")
            if tag_lower in [t.lower().strip() for t in tags]:
                d = dict(row)
                d["tags"] = json.loads(d["tags"] or "[]")
                d["ai_analysis"] = (
                    json.loads(d["ai_analysis"]) if d["ai_analysis"] else None
                )
                results.append(d)
    return results


def delete_article(article_id):
    with _connect() as conn:
        conn.execute("DELETE FROM saved_articles WHERE id = ?", (article_id,))
        conn.commit()
