"""
Connecteur vers le modèle IA de détection des Fake News.
Utilise un modèle Stacking + TF-IDF entraîné localement.
"""

import logging
from models.article import Article
from agent.database import DatabaseManager
from agent.model_loader import get_model_loader

logger = logging.getLogger(__name__)


class FakeNewsConnector:
    """
    Connecteur entre l'Agent collecteur et le modèle IA Fake News (Stacking + TF-IDF).

    Pipeline :
        Article → TF-IDF Vectorization → Stacking Classifier → Prédiction → DB
    """

    def __init__(self):
        self.db = DatabaseManager()
        self.model_loader = get_model_loader()
        
        if not self.model_loader.is_ready():
            logger.warning("⚠ Modèle Stacking non disponible, utilise mode dégradé")

    def prepare_text(self, article: Article) -> str:
        """
        Prépare le texte pour le modèle.
        Combine titre + contenu pour meilleure prédiction.
        """
        text = f"{article.title}. {article.content}"
        # Limite à 2000 caractères (TF-IDF recommandation)
        text = text[:2000]
        return text

    def predict(self, article: Article) -> dict:
        """
        Utilise le modèle Stacking + TF-IDF pour prédire si l'article est fake.

        Retourne :
            {
                "prediction": "real" | "fake",
                "confidence_score": 0.0 → 1.0
            }
        """
        try:
            # Préparer le texte
            text = self.prepare_text(article)
            
            # Prédire avec le modèle local
            result = self.model_loader.predict(text)
            
            prediction = result.get("prediction", "unknown")
            score = result.get("confidence_score", 0.0)
            
            if prediction != "error":
                logger.info(
                    f"[AI] '{article.title[:50]}' → {prediction.upper()} "
                    f"(confiance : {score*100:.1f}%)"
                )
                return {"prediction": prediction, "confidence_score": score}
            else:
                logger.error(f"[AI] Erreur de prédiction: {result.get('error')}")
                return {"prediction": None, "confidence_score": None}

        except Exception as e:
            logger.error(f"[AI] Erreur lors de la prédiction : {e}")
            return {"prediction": None, "confidence_score": None}

    def analyze_batch(self, articles: list[Article]) -> int:
        """
        Analyse un lot d'articles et met à jour la base de données.
        Retourne le nombre d'articles analysés avec succès.
        """
        success = 0
        for article in articles:
            result = self.predict(article)
            if result["prediction"]:
                self.db.update_prediction(
                    article.url,
                    result["prediction"],
                    result["confidence_score"],
                )
                success += 1
        logger.info(f"[AI] Lot traité : {success}/{len(articles)} articles analysés")
        return success

    def process_unanalyzed(self, limit: int = 50) -> int:
        """Récupère les articles sans prédiction et les envoie au modèle IA."""
        unanalyzed = self.db.get_unanalyzed(limit=limit)
        logger.info(f"[AI] {len(unanalyzed)} articles en attente d'analyse")

        from models.article import Article as ArticleModel
        articles = []
        for row in unanalyzed:
            a = ArticleModel(
                title=row["title"],
                content=row["content"] or "",
                url=row["url"],
                source=row["source"],
            )
            articles.append(a)

        return self.analyze_batch(articles)
