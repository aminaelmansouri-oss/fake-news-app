"""
Agent Collecteur Principal - Robot Journaliste Intelligent
Responsable de la collecte automatique des articles depuis le web.
"""

import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional
import logging
import time

from utils.cleaner import TextCleaner
from utils.deduplicator import Deduplicator
from utils.source_checker import SourceChecker
from config.settings import TRUSTED_SOURCES, REQUEST_HEADERS, REQUEST_TIMEOUT
from models.article import Article
from agent.database import DatabaseManager

logger = logging.getLogger(__name__)


class NewsCollectorAgent:
    """
    Agent principal de collecte des news.
    Pipeline : Crawl → Scrape → Clean → Deduplicate → Validate → Store
    """

    def __init__(self):
        self.cleaner = TextCleaner()
        self.deduplicator = Deduplicator()
        self.source_checker = SourceChecker()
        self.db = DatabaseManager()
        self.session = requests.Session()
        self.session.headers.update(REQUEST_HEADERS)

    # ─────────────────────────────────────────────
    # 1. COLLECTE DEPUIS LES FLUX RSS
    # ─────────────────────────────────────────────

    def collect_from_rss(self, rss_url: str, source_name: str) -> list[Article]:
        """Collecte les articles depuis un flux RSS."""
        articles = []
        logger.info(f"[RSS] Collecte depuis {source_name} → {rss_url}")

        try:
            feed = feedparser.parse(rss_url)
            for entry in feed.entries:
                article = self._parse_rss_entry(entry, source_name)
                if article:
                    articles.append(article)
        except Exception as e:
            logger.error(f"[RSS] Erreur pour {rss_url}: {e}")

        logger.info(f"[RSS] {len(articles)} articles collectés depuis {source_name}")
        return articles

    def _parse_rss_entry(self, entry, source_name: str) -> Optional[Article]:
        """Transforme une entrée RSS en objet Article."""
        try:
            url = entry.get("link", "")
            if not url:
                return None

            # Récupère le contenu complet si disponible
            content = entry.get("summary", "") or entry.get("content", [{}])[0].get("value", "")
            content_clean = self.cleaner.clean(content)

            return Article(
                title=self.cleaner.clean(entry.get("title", "Sans titre")),
                content=content_clean,
                url=url,
                source=source_name,
                author=entry.get("author", "Inconnu"),
                published_at=self._parse_date(entry.get("published", "")),
                category=entry.get("tags", [{}])[0].get("term", "General") if entry.get("tags") else "General",
            )
        except Exception as e:
            logger.warning(f"[RSS] Entrée ignorée: {e}")
            return None

    # ─────────────────────────────────────────────
    # 2. SCRAPING DES PAGES WEB
    # ─────────────────────────────────────────────

    def scrape_article(self, url: str, source_name: str) -> Optional[Article]:
        """Scrape le contenu complet d'un article depuis son URL."""
        logger.info(f"[SCRAPE] {url}")
        try:
            response = self.session.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            title = self._extract_title(soup)
            content = self._extract_content(soup)
            author = self._extract_author(soup)
            date = self._extract_date(soup)

            if not content or len(content) < 100:
                logger.warning(f"[SCRAPE] Contenu trop court pour {url}")
                return None

            return Article(
                title=self.cleaner.clean(title),
                content=self.cleaner.clean(content),
                url=url,
                source=source_name,
                author=author,
                published_at=date,
                category="General",
            )
        except requests.RequestException as e:
            logger.error(f"[SCRAPE] Erreur réseau pour {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extrait le titre de l'article."""
        for selector in ["h1.article-title", "h1.entry-title", "h1", "title"]:
            tag = soup.select_one(selector)
            if tag:
                return tag.get_text(strip=True)
        return "Sans titre"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extrait le texte principal de l'article."""
        # Suppression des éléments inutiles
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "ads", "form"]):
            tag.decompose()

        # Sélecteurs courants d'articles
        for selector in ["article", "div.article-body", "div.entry-content", "main", "div.content"]:
            block = soup.select_one(selector)
            if block:
                paragraphs = block.find_all("p")
                return " ".join(p.get_text(strip=True) for p in paragraphs)

        return soup.get_text(separator=" ", strip=True)

    def _extract_author(self, soup: BeautifulSoup) -> str:
        """Extrait l'auteur de l'article."""
        for selector in [
            'meta[name="author"]',
            'span.author',
            'a[rel="author"]',
            'div.byline',
        ]:
            tag = soup.select_one(selector)
            if tag:
                return tag.get("content", tag.get_text(strip=True))
        return "Inconnu"

    def _extract_date(self, soup: BeautifulSoup) -> Optional[datetime]:
        """Extrait la date de publication."""
        tag = soup.select_one('meta[property="article:published_time"]') or \
              soup.select_one('time[datetime]')
        if tag:
            raw = tag.get("content") or tag.get("datetime", "")
            return self._parse_date(raw)
        return datetime.utcnow()

    def _parse_date(self, raw: str) -> Optional[datetime]:
        """Convertit une chaîne de date en objet datetime."""
        for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"]:
            try:
                return datetime.strptime(raw[:len(fmt)], fmt)
            except (ValueError, TypeError):
                continue
        return datetime.utcnow()

    # ─────────────────────────────────────────────
    # 3. PIPELINE COMPLET
    # ─────────────────────────────────────────────

    def run_pipeline(self, sources: list[dict]) -> dict:
        """
        Pipeline principal :
        Collecte → Nettoyage → Déduplication → Validation → Stockage
        """
        logger.info("=" * 60)
        logger.info("DÉMARRAGE DU PIPELINE DE COLLECTE")
        logger.info("=" * 60)

        all_articles = []
        stats = {"collected": 0, "duplicates": 0, "invalid_source": 0, "stored": 0}

        # Étape 1 : Collecte
        for source in sources:
            if source.get("type") == "rss":
                articles = self.collect_from_rss(source["url"], source["name"])
            else:
                article = self.scrape_article(source["url"], source["name"])
                articles = [article] if article else []
            all_articles.extend(articles)
            time.sleep(1)  # Respect des serveurs

        stats["collected"] = len(all_articles)

        # Étape 2 : Déduplication
        unique_articles = self.deduplicator.filter_duplicates(all_articles)
        stats["duplicates"] = stats["collected"] - len(unique_articles)

        # Étape 3 : Vérification des sources
        trusted_articles = [
            a for a in unique_articles
            if self.source_checker.is_trusted(a.source)
        ]
        stats["invalid_source"] = len(unique_articles) - len(trusted_articles)

        # Étape 4 : Stockage
        for article in trusted_articles:
            self.db.save_article(article)
            stats["stored"] += 1

        logger.info(f"PIPELINE TERMINÉ — {stats}")
        return stats
