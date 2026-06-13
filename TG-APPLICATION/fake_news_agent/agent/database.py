"""
Module de gestion de la base de données.
Sauvegarde les articles collectés, nettoyés et scorés par l'IA.
"""

import sqlite3
import logging
from datetime import datetime
from models.article import Article
from config.settings import DATABASE_URL

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Gère la persistance des articles dans SQLite (ou PostgreSQL via URL).
    """

    def __init__(self, db_path: str = "fake_news_agent.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Crée la table articles si elle n'existe pas."""
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    title       TEXT NOT NULL,
                    content     TEXT,
                    url         TEXT UNIQUE,
                    source      TEXT,
                    author      TEXT,
                    category    TEXT,
                    published_at TEXT,
                    prediction  TEXT,
                    score       REAL,
                    collected_at TEXT
                )
            """)
        logger.info("[DB] Base de données initialisée.")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def save_article(self, article: Article) -> bool:
        """Sauvegarde un article. Ignore les doublons (URL unique)."""
        try:
            with self._connect() as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO articles
                    (title, content, url, source, author, category,
                     published_at, prediction, score, collected_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    article.title,
                    article.content,
                    article.url,
                    article.source,
                    article.author,
                    article.category,
                    article.published_at.isoformat() if article.published_at else None,
                    article.prediction,
                    article.confidence_score,
                    article.collected_at.isoformat(),
                ))
            logger.debug(f"[DB] Article sauvegardé : '{article.title[:50]}'")
            return True
        except Exception as e:
            logger.error(f"[DB] Erreur sauvegarde : {e}")
            return False

    def update_prediction(self, url: str, prediction: str, score: float):
        """Met à jour la prédiction IA d'un article existant."""
        with self._connect() as conn:
            conn.execute(
                "UPDATE articles SET prediction=?, score=? WHERE url=?",
                (prediction, score, url)
            )
        logger.info(f"[DB] Prédiction mise à jour : {url} → {prediction} ({score:.2f})")

    def get_unanalyzed(self, limit: int = 50) -> list[dict]:
        """Retourne les articles sans prédiction IA."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE prediction IS NULL LIMIT ?", (limit,)
            ).fetchall()
        return [dict(row) for row in rows]

    def get_by_category(self, category: str, limit: int = 20) -> list[dict]:
        """Retourne les articles d'une catégorie donnée."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE category=? ORDER BY published_at DESC LIMIT ?",
                (category, limit)
            ).fetchall()
        return [dict(row) for row in rows]

    def get_stats(self) -> dict:
        """Retourne des statistiques globales sur la base."""
        with self._connect() as conn:
            total = conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
            real  = conn.execute("SELECT COUNT(*) FROM articles WHERE prediction='real'").fetchone()[0]
            fake  = conn.execute("SELECT COUNT(*) FROM articles WHERE prediction='fake'").fetchone()[0]
            unanalyzed = conn.execute("SELECT COUNT(*) FROM articles WHERE prediction IS NULL").fetchone()[0]
        return {
            "total": total,
            "real": real,
            "fake": fake,
            "unanalyzed": unanalyzed,
        }

    def get_real_articles(self, limit: int = 20, skip: int = 0) -> list[dict]:
        """Retourne les articles identifiés comme REAL (vrais)."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE prediction='real' ORDER BY collected_at DESC LIMIT ? OFFSET ?",
                (limit, skip)
            ).fetchall()
        return [dict(row) for row in rows]

    def get_fake_articles(self, limit: int = 20, skip: int = 0) -> list[dict]:
        """Retourne les articles identifiés comme FAKE (faux)."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE prediction='fake' ORDER BY collected_at DESC LIMIT ? OFFSET ?",
                (limit, skip)
            ).fetchall()
        return [dict(row) for row in rows]

    def get_all_articles(self, limit: int = 20, skip: int = 0) -> list[dict]:
        """Retourne tous les articles (real + fake)."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM articles WHERE prediction IS NOT NULL ORDER BY collected_at DESC LIMIT ? OFFSET ?",
                (limit, skip)
            ).fetchall()
        return [dict(row) for row in rows]
