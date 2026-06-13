"""
Chargeur du modèle Stacking + TF-IDF entraîné.
Responsable de charger les artefacts du modèle depuis le dossier models/.
"""

import os
import joblib
import pickle
import json
import logging
from typing import Optional, Tuple, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Gestionnaire de chargement et d'utilisation du modèle Stacking entraîné.
    """

    def __init__(self, model_dir: str = "fake_news_models"):
        """
        Initialise le chargeur de modèles.
        
        Args:
            model_dir: Chemin du dossier contenant les modèles sauvegardés
        """
        # Si le chemin est relatif et commence par "fake_news_models",
        # remontez d'un niveau pour trouver le répertoire racine du projet
        if not os.path.isabs(model_dir):
            # Chemin du fichier courant (model_loader.py)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Remontez deux niveaux: agent/ -> fake_news_agent/ -> racine/
            project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
            model_dir = os.path.join(project_root, model_dir)
        
        self.model_dir = model_dir
        self.model = None
        self.vectorizer = None
        self.metadata = None
        self._load_model_artifacts()

    def _load_model_artifacts(self) -> None:
        """Charge tous les artefacts du modèle depuis les fichiers."""
        try:
            # Chemins possibles pour le modèle (essayer .pkl et .joblib)
            model_pkl_path = os.path.join(self.model_dir, "stacking_classifier_tfidf.pkl")
            model_joblib_path = os.path.join(self.model_dir, "stacking_classifier_tfidf.joblib")
            
            # Chemins possibles pour le vectorizer
            vectorizer_pkl_path = os.path.join(self.model_dir, "tfidf_vectorizer.pkl")
            vectorizer_joblib_path = os.path.join(self.model_dir, "tfidf_vectorizer.joblib")
            
            metadata_path = os.path.join(self.model_dir, "model_metadata.json")

            # Charger le modèle (essayer .pkl d'abord, puis .joblib)
            if os.path.exists(model_pkl_path):
                with open(model_pkl_path, 'rb') as f:
                    self.model = pickle.load(f)
                logger.info(f"✓ Modèle Stacking chargé (pickle): {model_pkl_path}")
            elif os.path.exists(model_joblib_path):
                self.model = joblib.load(model_joblib_path)
                logger.info(f"✓ Modèle Stacking chargé (joblib): {model_joblib_path}")
            else:
                logger.warning(f"⚠ Modèle non trouvé: {model_pkl_path} ou {model_joblib_path}")

            # Charger le vectorizer (essayer .pkl d'abord, puis .joblib)
            if os.path.exists(vectorizer_pkl_path):
                with open(vectorizer_pkl_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                logger.info(f"✓ Vectorizer TF-IDF chargé (pickle): {vectorizer_pkl_path}")
            elif os.path.exists(vectorizer_joblib_path):
                self.vectorizer = joblib.load(vectorizer_joblib_path)
                logger.info(f"✓ Vectorizer TF-IDF chargé (joblib): {vectorizer_joblib_path}")
            else:
                logger.warning(f"⚠ Vectorizer non trouvé: {vectorizer_pkl_path} ou {vectorizer_joblib_path}")

            # Charger les métadonnées
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                logger.info(f"✓ Métadonnées chargées: {metadata_path}")
            else:
                logger.warning(f"⚠ Métadonnées non trouvées: {metadata_path}")

        except Exception as e:
            logger.error(f"✗ Erreur lors du chargement des artefacts: {e}")
            raise

    def is_ready(self) -> bool:
        """Vérifie si le modèle est prêt à faire des prédictions."""
        return self.model is not None and self.vectorizer is not None

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Prédit si un texte est un fake ou real news.
        
        Args:
            text: Texte de l'article à analyser
            
        Returns:
            {
                "prediction": "real" | "fake",
                "confidence_score": 0.0-1.0,
                "model_name": "Stacking Classifier",
                "is_fake": bool
            }
        """
        if not self.is_ready():
            return {
                "prediction": "unknown",
                "confidence_score": 0.0,
                "error": "Modèle non initialisé"
            }

        try:
            # Vectoriser le texte
            X_vectorized = self.vectorizer.transform([text])

            # Prédire
            prediction_label = self.model.predict(X_vectorized)[0]
            probabilities = self.model.predict_proba(X_vectorized)[0]

            # Formater les résultats
            # Le modèle peut retourner soit des strings ('real'/'fake') soit des nombres (0/1)
            if isinstance(prediction_label, str):
                prediction_str = prediction_label
                is_fake = prediction_label == 'fake'
            else:
                # Si nombres: 0='real', 1='fake'
                prediction_str = "fake" if prediction_label == 1 else "real"
                is_fake = prediction_label == 1
            
            confidence = float(max(probabilities))

            return {
                "prediction": prediction_str,
                "confidence_score": confidence,
                "is_fake": is_fake,
                "probabilities": {
                    "real": float(probabilities[0]),
                    "fake": float(probabilities[1])
                },
                "model_name": "Stacking Classifier (TF-IDF)"
            }

        except Exception as e:
            logger.error(f"✗ Erreur lors de la prédiction: {e}")
            return {
                "prediction": "error",
                "confidence_score": 0.0,
                "error": str(e)
            }

    def predict_batch(self, texts: list) -> list:
        """
        Prédit pour plusieurs textes en batch.
        
        Args:
            texts: Liste de textes à analyser
            
        Returns:
            Liste de dictionnaires avec prédictions
        """
        if not self.is_ready():
            logger.error("Modèle non initialisé")
            return []

        results = []
        try:
            # Vectoriser tous les textes
            X_vectorized = self.vectorizer.transform(texts)

            # Prédictions batch
            predictions = self.model.predict(X_vectorized)
            probabilities = self.model.predict_proba(X_vectorized)

            for i, (pred, proba) in enumerate(zip(predictions, probabilities)):
                # Gérer les labels strings ou numériques
                if isinstance(pred, str):
                    prediction_str = pred
                    is_fake = pred == 'fake'
                else:
                    prediction_str = "fake" if pred == 1 else "real"
                    is_fake = pred == 1
                    
                results.append({
                    "text": texts[i][:100],  # Preview
                    "prediction": prediction_str,
                    "confidence_score": float(max(proba)),
                    "is_fake": is_fake
                })

            logger.info(f"✓ {len(results)} prédictions batch effectuées")
            return results

        except Exception as e:
            logger.error(f"✗ Erreur lors des prédictions batch: {e}")
            return []

    def get_model_info(self) -> Dict[str, Any]:
        """Retourne les informations du modèle."""
        if self.metadata is None:
            return {"status": "Métadonnées non disponibles"}

        return {
            "model_name": self.metadata.get("model_name"),
            "model_type": self.metadata.get("model_type"),
            "base_learners": self.metadata.get("base_learners"),
            "meta_learner": self.metadata.get("meta_learner"),
            "training_date": self.metadata.get("training_date"),
            "test_metrics": self.metadata.get("test_set_metrics"),
            "vectorizer": self.metadata.get("vectorizer"),
            "total_features": self.metadata.get("total_features")
        }


# Singleton global
_model_loader = None


def get_model_loader() -> ModelLoader:
    """Retourne l'instance unique du ModelLoader (pattern Singleton)."""
    global _model_loader
    if _model_loader is None:
        _model_loader = ModelLoader()
    return _model_loader
