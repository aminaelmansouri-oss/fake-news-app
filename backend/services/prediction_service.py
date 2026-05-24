import pickle
import numpy as np
from pathlib import Path
from scipy.sparse import hstack

MODEL_DIR = Path(__file__).parent.parent / "model"

# Lazy-loaded globals
_model = None
_word_tfidf = None
_char_tfidf = None


def _load_models():
    global _model, _word_tfidf, _char_tfidf
    if _model is None:
        try:
            with open(MODEL_DIR / "fake_news_model.pkl", "rb") as f:
                _model = pickle.load(f)
            with open(MODEL_DIR / "vectorizer_word.pkl", "rb") as f:
                _word_tfidf = pickle.load(f)
            with open(MODEL_DIR / "vectorizer_char.pkl", "rb") as f:
                _char_tfidf = pickle.load(f)
            print("[PredictionService] Models loaded successfully.")
        except FileNotFoundError:
            print("[PredictionService] Model files not found. Running trainer...")
            import sys
            sys.path.insert(0, str(MODEL_DIR))
            from model.train_model import train_and_save
            train_and_save()
            # Retry load
            with open(MODEL_DIR / "fake_news_model.pkl", "rb") as f:
                _model = pickle.load(f)
            with open(MODEL_DIR / "vectorizer_word.pkl", "rb") as f:
                _word_tfidf = pickle.load(f)
            with open(MODEL_DIR / "vectorizer_char.pkl", "rb") as f:
                _char_tfidf = pickle.load(f)


def predict(text: str) -> dict:
    """
    Predict whether a given text is fake or real news.
    Returns a dict with prediction, confidence, and scores.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from preprocessing.clean_text import clean_text

    _load_models()

    cleaned = clean_text(text)
    word_count = len(text.split())

    if len(cleaned.strip()) < 5:
        return {
            "error": "Text is too short or contains no meaningful content after cleaning."
        }

    X_word = _word_tfidf.transform([cleaned])
    X_char = _char_tfidf.transform([cleaned])
    X = hstack([X_word, X_char])

    proba = _model.predict_proba(X)[0]
    fake_score = float(proba[0])
    real_score = float(proba[1])

    prediction = "REAL" if real_score > fake_score else "FAKE"
    confidence = max(fake_score, real_score)

    # Confidence band
    if confidence >= 0.85:
        confidence_label = "High"
    elif confidence >= 0.65:
        confidence_label = "Medium"
    else:
        confidence_label = "Low"

    return {
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "confidence_label": confidence_label,
        "confidence_pct": round(confidence * 100, 1),
        "fake_score": round(fake_score, 4),
        "real_score": round(real_score, 4),
        "fake_pct": round(fake_score * 100, 1),
        "real_pct": round(real_score * 100, 1),
        "word_count": word_count,
        "text_preview": text[:200]
    }
