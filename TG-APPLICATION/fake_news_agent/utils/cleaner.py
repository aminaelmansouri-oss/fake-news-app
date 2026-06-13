"""
Module de nettoyage des textes bruts collectés.
Supprime HTML, balises, publicités, caractères spéciaux, espaces inutiles.
"""

import re
import html
import unicodedata


class TextCleaner:
    """
    Nettoie et normalise les textes bruts collectés depuis le web.

    Exemple :
        Avant : "BREAKING!!! Click HERE!!! <b>Read more</b>   "
        Après : "Breaking. Click here. Read more"
    """

    # Patterns de nettoyage
    HTML_TAG_RE = re.compile(r"<[^>]+>")
    MULTIPLE_SPACES_RE = re.compile(r"\s{2,}")
    SPECIAL_CHARS_RE = re.compile(r"[^\w\s\.\,\!\?\;\:\'\"\-]")
    EXCLAMATIONS_RE = re.compile(r"!{2,}")
    QUESTION_MARKS_RE = re.compile(r"\?{2,}")

    # Mots clés typiques des publicités/clickbait à supprimer
    CLICKBAIT_PATTERNS = [
        r"CLICK\s+HERE",
        r"READ\s+MORE",
        r"SUBSCRIBE\s+NOW",
        r"ADVERTISEMENT",
        r"SPONSORED",
        r"PROMOTED",
    ]

    def clean(self, text: str) -> str:
        """Pipeline complet de nettoyage d'un texte."""
        if not text:
            return ""

        text = self._decode_html_entities(text)
        text = self._remove_html_tags(text)
        text = self._remove_clickbait(text)
        text = self._normalize_punctuation(text)
        text = self._normalize_whitespace(text)
        text = self._normalize_case(text)
        text = self._normalize_unicode(text)

        return text.strip()

    def _decode_html_entities(self, text: str) -> str:
        """Décode les entités HTML : &amp; → & / &nbsp; → espace."""
        return html.unescape(text)

    def _remove_html_tags(self, text: str) -> str:
        """Supprime toutes les balises HTML."""
        return self.HTML_TAG_RE.sub(" ", text)

    def _remove_clickbait(self, text: str) -> str:
        """Supprime les formules typiques du clickbait."""
        for pattern in self.CLICKBAIT_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.IGNORECASE)
        return text

    def _normalize_punctuation(self, text: str) -> str:
        """Normalise les ponctuations excessives."""
        text = self.EXCLAMATIONS_RE.sub("!", text)
        text = self.QUESTION_MARKS_RE.sub("?", text)
        return text

    def _normalize_whitespace(self, text: str) -> str:
        """Supprime les espaces et sauts de ligne multiples."""
        text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        return self.MULTIPLE_SPACES_RE.sub(" ", text)

    def _normalize_case(self, text: str) -> str:
        """Corrige les textes entièrement en majuscules."""
        if text.isupper() and len(text) > 5:
            return text.capitalize()
        return text

    def _normalize_unicode(self, text: str) -> str:
        """Normalise l'encodage Unicode (supprime les caractères bizarres)."""
        return unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
