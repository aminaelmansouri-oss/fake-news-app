"""
Module de détection et suppression des articles dupliqués.
Utilise la comparaison de titres et la similarité textuelle (Jaccard).
"""

import hashlib
import logging
from difflib import SequenceMatcher
from models.article import Article

logger = logging.getLogger(__name__)


class Deduplicator:
    """
    Détecte les articles dupliqués selon deux stratégies :
    1. Hash exact de l'URL
    2. Similarité du titre (seuil configurable)
    """

    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self._seen_urls: set[str] = set()
        self._seen_titles: list[str] = []

    def is_duplicate(self, article: Article) -> bool:
        """Retourne True si l'article est un doublon."""
        # Vérification par URL exacte
        url_hash = hashlib.md5(article.url.encode()).hexdigest()
        if url_hash in self._seen_urls:
            logger.debug(f"[DEDUP] Doublon URL : {article.url}")
            return True

        # Vérification par similarité de titre
        for existing_title in self._seen_titles:
            similarity = self._title_similarity(article.title, existing_title)
            if similarity >= self.similarity_threshold:
                logger.debug(
                    f"[DEDUP] Titre similaire ({similarity:.0%}) : '{article.title[:50]}'"
                )
                return True

        # Enregistrement pour les prochains articles
        self._seen_urls.add(url_hash)
        self._seen_titles.append(article.title)
        return False

    def filter_duplicates(self, articles: list[Article]) -> list[Article]:
        """Filtre une liste d'articles en supprimant les doublons."""
        unique = []
        for article in articles:
            if not self.is_duplicate(article):
                unique.append(article)
            else:
                article.is_duplicate = True

        removed = len(articles) - len(unique)
        logger.info(f"[DEDUP] {removed} doublon(s) supprimé(s) sur {len(articles)} articles")
        return unique

    def _title_similarity(self, title_a: str, title_b: str) -> float:
        """Calcule la similarité entre deux titres (Jaccard sur les mots)."""
        words_a = set(title_a.lower().split())
        words_b = set(title_b.lower().split())
        if not words_a or not words_b:
            return 0.0
        intersection = words_a & words_b
        union = words_a | words_b
        return len(intersection) / len(union)

    def reset(self):
        """Réinitialise le cache de doublons (utile entre deux collectes)."""
        self._seen_urls.clear()
        self._seen_titles.clear()
