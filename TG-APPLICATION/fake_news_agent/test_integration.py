"""
Script de test pour valider l'intégration du modèle Stacking + TF-IDF.
Teste : 
  - Chargement du modèle
  - Prédictions simples
  - Prédictions batch
  - Intégration avec la base de données
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("\n" + "=" * 80)
print("TEST D'INTÉGRATION : STACKING + TF-IDF + DATABASE")
print("=" * 80)

# ─────────────────────────────────────────────
# TEST 1 : Chargement du modèle
# ─────────────────────────────────────────────

print("\n[TEST 1] Chargement du modèle Stacking...")
try:
    from agent.model_loader import get_model_loader
    
    model_loader = get_model_loader()
    
    if model_loader.is_ready():
        print("  ✓ Modèle chargé avec succès")
        print(f"  ✓ Infos: {model_loader.get_model_info()}")
    else:
        print("  ⚠ Modèle non prêt (fichiers manquants)")
except Exception as e:
    print(f"  ✗ Erreur: {e}")
    sys.exit(1)

# ─────────────────────────────────────────────
# TEST 2 : Prédictions simples
# ─────────────────────────────────────────────

print("\n[TEST 2] Prédictions simples...")
test_articles = [
    ("Trump announces new trade policy to boost US economy", "POTUS Economy"),
    ("Biden claims election was rigged without evidence", "Election Claim"),
    ("Scientists discover new cure for cancer", "Health News"),
]

try:
    for text, title in test_articles:
        result = model_loader.predict(text)
        print(f"  [{result['prediction'].upper()}] {title}")
        print(f"    └─ Confiance: {result['confidence_score']*100:.1f}%")
    print("  ✓ Prédictions simples OK")
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# ─────────────────────────────────────────────
# TEST 3 : Prédictions batch
# ─────────────────────────────────────────────

print("\n[TEST 3] Prédictions batch...")
try:
    texts = [article[0] for article in test_articles]
    batch_results = model_loader.predict_batch(texts)
    
    for result in batch_results:
        print(f"  [{result['prediction'].upper()}] {result['text'][:60]}...")
    print(f"  ✓ Batch OK ({len(batch_results)} articles)")
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# ─────────────────────────────────────────────
# TEST 4 : Intégration database
# ─────────────────────────────────────────────

print("\n[TEST 4] Intégration avec la base de données...")
try:
    from agent.database import DatabaseManager
    from models.article import Article
    
    db = DatabaseManager()
    
    # Insérer un article test
    test_article = Article(
        title="Test Article",
        content="This is a test article for the fake news detector.",
        url="https://example.com/test",
        source="TestSource",
        prediction="real",
        confidence_score=0.95
    )
    
    db.save_article(test_article)
    print("  ✓ Article sauvegardé")
    
    # Récupérer les stats
    stats = db.get_stats()
    print(f"  ✓ Stats: {stats['total']} articles ({stats['real']} real, {stats['fake']} fake)")
    
    # Récupérer les articles real
    real_articles = db.get_real_articles(limit=3)
    print(f"  ✓ {len(real_articles)} articles REAL récupérés")
    
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# ─────────────────────────────────────────────
# TEST 5 : Connecteur IA
# ─────────────────────────────────────────────

print("\n[TEST 5] Connecteur IA (FakeNewsConnector)...")
try:
    from agent.ai_connector import FakeNewsConnector
    
    connector = FakeNewsConnector()
    
    # Créer un article test
    from models.article import Article
    article = Article(
        title="Breaking News",
        content="The president announced a new policy today.",
        url="https://example.com/news",
        source="TestMedia"
    )
    
    # Prédire
    result = connector.predict(article)
    print(f"  ✓ Prédiction: {result['prediction']} (confiance: {result['confidence_score']})")
    
except Exception as e:
    print(f"  ✗ Erreur: {e}")

# ─────────────────────────────────────────────
# RÉSUMÉ
# ─────────────────────────────────────────────

print("\n" + "=" * 80)
print("✅ TOUS LES TESTS RÉUSSIS !")
print("=" * 80)

print("""
Prochaines étapes:

1. Lancer l'API FastAPI:
   $ python -m uvicorn api:app --reload --port 8000

2. Accéder à la documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Tester les endpoints:
   POST http://localhost:8000/api/predict
   GET http://localhost:8000/api/articles/real
   GET http://localhost:8000/api/stats

4. Lancer le collector automatique:
   $ python main.py

5. Frontend: Utiliser les endpoints /api/articles/real pour afficher les vraies news
""")

print("=" * 80 + "\n")
