import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "truthguard-secret-2024")
    DEBUG = os.environ.get("DEBUG", "True") == "True"
    
    # Model paths
    MODEL_PATH = BASE_DIR / "model" / "fake_news_model.pkl"
    VECTORIZER_WORD_PATH = BASE_DIR / "model" / "vectorizer_word.pkl"
    VECTORIZER_CHAR_PATH = BASE_DIR / "model" / "vectorizer_char.pkl"
    
    # Database
    DB_PATH = BASE_DIR / "database" / "history.db"
    
    # Scraping
    SCRAPE_TIMEOUT = 10
    MAX_TEXT_LENGTH = 5000
    
    # CORS
    CORS_ORIGINS = ["http://localhost:5500", "http://127.0.0.1:5500", "*"]
