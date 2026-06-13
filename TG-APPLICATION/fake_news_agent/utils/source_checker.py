"""
Module de vérification de la crédibilité des sources.
Vérifie si une source appartient à la whitelist des médias fiables.
"""

import logging
from config.settings import TRUSTED_SOURCES

logger = logging.getLogger(__name__)


class SourceChecker:
    """
    Vérifie la réputation et la crédibilité des sources d'actualité.

    Whitelist configurée dans config/settings.py
    """

    def __init__(self, extra_trusted: list[str] = None):
        self.trusted = set(TRUSTED_SOURCES)
        if extra_trusted:
            self.trusted.update(extra_trusted)

    def is_trusted(self, source_name: str) -> bool:
        """Retourne True si la source est dans la whitelist."""
        source_lower = source_name.lower().strip()
        for trusted in self.trusted:
            if trusted.lower() in source_lower or source_lower in trusted.lower():
                return True
        logger.warning(f"[SOURCE] Source non fiable ignorée : '{source_name}'")
        return False

    def add_trusted(self, source: str):
        """Ajoute une source à la whitelist."""
        self.trusted.add(source.lower())
        logger.info(f"[SOURCE] Source ajoutée à la whitelist : {source}")

    def get_all_trusted(self) -> list[str]:
        """Retourne la liste complète des sources fiables."""
        return sorted(list(self.trusted))
