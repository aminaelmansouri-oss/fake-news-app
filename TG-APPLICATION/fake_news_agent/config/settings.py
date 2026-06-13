"""
Configuration centrale de l'Agent Collecteur.
Toutes les constantes modifiables sont définies ici.
"""

# ─────────────────────────────────────────────
# SOURCES DE CONFIANCE (WHITELIST)
# ─────────────────────────────────────────────
TRUSTED_SOURCES = [
    "BBC",
    "Reuters",
    "CNN",
    "Al Jazeera",
    "The Guardian",
    "Associated Press",
    "AFP",
    "Le Monde",
    "France 24",
    "DW",
    "NPR",
]

# ─────────────────────────────────────────────
# FLUX RSS PAR DÉFAUT
# ─────────────────────────────────────────────
DEFAULT_RSS_SOURCES = [
    {"name": "BBC",     "url": "http://feeds.bbci.co.uk/news/rss.xml",          "type": "rss"},
    {"name": "Reuters", "url": "https://feeds.reuters.com/reuters/topNews",      "type": "rss"},
    {"name": "CNN",     "url": "http://rss.cnn.com/rss/edition.rss",             "type": "rss"},
    {"name": "Al Jazeera", "url": "https://www.aljazeera.com/xml/rss/all.xml",  "type": "rss"},
    {"name": "DW",      "url": "https://rss.dw.com/rdf/rss-en-all",             "type": "rss"},
]

# ─────────────────────────────────────────────
# PARAMÈTRES HTTP
# ─────────────────────────────────────────────
REQUEST_TIMEOUT = 10  # secondes
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; FakeNewsAgent/1.0; +https://example.com/bot)"
    ),
    "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
}

# ─────────────────────────────────────────────
# BASE DE DONNÉES
# ─────────────────────────────────────────────
DATABASE_URL = "sqlite:///fake_news_agent.db"
# Pour PostgreSQL : "postgresql://user:password@localhost:5432/fake_news"

# ─────────────────────────────────────────────
# DÉDUPLICATION
# ─────────────────────────────────────────────
SIMILARITY_THRESHOLD = 0.85  # Seuil de similarité entre titres (0.0 → 1.0)

# ─────────────────────────────────────────────
# PLANIFICATEUR (SCHEDULER)
# ─────────────────────────────────────────────
SCHEDULER_INTERVAL_HOURS = 1  # Collecte toutes les X heures

# ─────────────────────────────────────────────
# MODÈLE IA FAKE NEWS
# ─────────────────────────────────────────────
FAKE_NEWS_MODEL_ENDPOINT = "http://localhost:8000/api/predict"
FAKE_NEWS_MODEL_TIMEOUT = 30

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────
LOG_LEVEL = "INFO"
LOG_FILE = "logs/agent.log"
