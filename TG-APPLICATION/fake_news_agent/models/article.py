"""
Modèle de données Article - Structure unifiée de tous les articles collectés.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Article:
    """Représente un article collecté, nettoyé et structuré."""

    title: str
    content: str
    url: str
    source: str
    author: str = "Inconnu"
    published_at: Optional[datetime] = None
    category: str = "General"

    # Champs ajoutés par le modèle IA
    prediction: Optional[str] = None       # "real" ou "fake"
    confidence_score: Optional[float] = None  # entre 0.0 et 1.0

    # Méta-données internes
    collected_at: datetime = field(default_factory=datetime.utcnow)
    is_duplicate: bool = False

    def to_dict(self) -> dict:
        """Sérialise l'article en dictionnaire JSON-compatible."""
        return {
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "source": self.source,
            "author": self.author,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "category": self.category,
            "prediction": self.prediction,
            "confidence_score": self.confidence_score,
            "collected_at": self.collected_at.isoformat(),
        }

    def __repr__(self):
        return f"<Article [{self.source}] '{self.title[:60]}...'>"
