"""
Tests unitaires de l'Agent Collecteur.
Couvre : nettoyage, déduplication, vérification des sources, modèle Article.
"""

import pytest
from utils.cleaner import TextCleaner
from utils.deduplicator import Deduplicator
from utils.source_checker import SourceChecker
from models.article import Article


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def cleaner():
    return TextCleaner()

@pytest.fixture
def dedup():
    return Deduplicator(similarity_threshold=0.85)

@pytest.fixture
def checker():
    return SourceChecker()

def make_article(title="Test Article", url="https://bbc.com/test", source="BBC"):
    return Article(title=title, content="Sample content.", url=url, source=source)


# ─────────────────────────────────────────────
# TESTS : TextCleaner
# ─────────────────────────────────────────────

class TestTextCleaner:

    def test_removes_html_tags(self, cleaner):
        result = cleaner.clean("<b>Hello</b> <i>World</i>")
        assert "<b>" not in result
        assert "Hello" in result

    def test_decodes_html_entities(self, cleaner):
        result = cleaner.clean("&amp; &nbsp; &lt;")
        assert "&amp;" not in result

    def test_normalizes_multiple_exclamations(self, cleaner):
        result = cleaner.clean("BREAKING!!!")
        assert "!!!" not in result

    def test_strips_whitespace(self, cleaner):
        result = cleaner.clean("  hello   world  ")
        assert result == result.strip()
        assert "  " not in result

    def test_handles_empty_string(self, cleaner):
        assert cleaner.clean("") == ""

    def test_handles_none(self, cleaner):
        assert cleaner.clean(None) == ""


# ─────────────────────────────────────────────
# TESTS : Deduplicator
# ─────────────────────────────────────────────

class TestDeduplicator:

    def test_unique_articles_pass(self, dedup):
        a1 = make_article("Article A", "https://bbc.com/a")
        a2 = make_article("Article B", "https://bbc.com/b")
        result = dedup.filter_duplicates([a1, a2])
        assert len(result) == 2

    def test_same_url_is_duplicate(self, dedup):
        a1 = make_article("Title One", "https://bbc.com/same")
        a2 = make_article("Title Two", "https://bbc.com/same")
        result = dedup.filter_duplicates([a1, a2])
        assert len(result) == 1

    def test_similar_title_is_duplicate(self, dedup):
        a1 = make_article("France wins the World Cup final", "https://bbc.com/1")
        a2 = make_article("France wins the World Cup final tonight", "https://cnn.com/2")
        result = dedup.filter_duplicates([a1, a2])
        assert len(result) == 1

    def test_different_titles_are_unique(self, dedup):
        a1 = make_article("Climate change summit begins", "https://bbc.com/1")
        a2 = make_article("Election results in Argentina", "https://cnn.com/2")
        result = dedup.filter_duplicates([a1, a2])
        assert len(result) == 2


# ─────────────────────────────────────────────
# TESTS : SourceChecker
# ─────────────────────────────────────────────

class TestSourceChecker:

    def test_trusted_source_passes(self, checker):
        assert checker.is_trusted("BBC") is True
        assert checker.is_trusted("Reuters") is True
        assert checker.is_trusted("CNN") is True

    def test_unknown_source_rejected(self, checker):
        assert checker.is_trusted("FakeNewsDaily") is False
        assert checker.is_trusted("RandomBlog123") is False

    def test_add_trusted_source(self, checker):
        checker.add_trusted("TechCrunch")
        assert checker.is_trusted("TechCrunch") is True


# ─────────────────────────────────────────────
# TESTS : Article Model
# ─────────────────────────────────────────────

class TestArticleModel:

    def test_to_dict_has_required_keys(self):
        article = make_article()
        d = article.to_dict()
        for key in ["title", "content", "url", "source", "prediction", "confidence_score"]:
            assert key in d

    def test_repr_contains_source(self):
        article = make_article(source="Reuters")
        assert "Reuters" in repr(article)
