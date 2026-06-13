"""
API FastAPI pour détection de Fake News et récupération des articles.
Endpoints pour :
  - Prédictions individuelles et batch
  - Récupération des articles (real/fake)
  - Statistiques de la base
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import logging
from datetime import datetime

from agent.model_loader import get_model_loader
from agent.database import DatabaseManager
from agent.collector import NewsCollectorAgent
from agent.ai_connector import FakeNewsConnector
from config.settings import DEFAULT_RSS_SOURCES

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialiser FastAPI
app = FastAPI(
    title="Fake News Detection API",
    description="API pour la détection de fake news et la gestion d'actualités",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiser les gestionnaires
db_manager = DatabaseManager()
model_loader = get_model_loader()
fake_news_connector = FakeNewsConnector()

# Try to locate the frontend build (Vite) and mount it as static files.
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, "frontend", "dist"))
if os.path.isdir(FRONTEND_DIST):
    # Will be mounted after all routes are defined
    pass
else:
    FRONTEND_DIST = None


# ─────────────────────────────────────────────
# MODÈLES PYDANTIC
# ─────────────────────────────────────────────

class PredictionRequest(BaseModel):
    """Requête de prédiction pour un article."""
    text: str
    title: Optional[str] = None
    source: Optional[str] = "Unknown"


class PredictionResponse(BaseModel):
    """Réponse de prédiction."""
    prediction: str  # "real" ou "fake"
    confidence_score: float
    is_fake: bool
    model_name: str
    probabilities: dict


class ArticleResponse(BaseModel):
    """Réponse pour un article de la base."""
    id: int
    title: str
    source: str
    prediction: Optional[str]
    score: Optional[float]
    published_at: Optional[str]
    collected_at: str


class StatsResponse(BaseModel):
    """Statistiques de la base de données."""
    total: int
    real: int
    fake: int
    unanalyzed: int


# ─────────────────────────────────────────────
# ENDPOINTS PRÉDICTIONS
# ─────────────────────────────────────────────

@app.post("/api/predict", response_model=dict)
async def predict(request: PredictionRequest):
    """
    Prédit si un texte est un fake ou real news.
    
    Exemple:
    ```
    POST /api/predict
    {
        "text": "Le président annonce une nouvelle politique...",
        "title": "Nouvelle décision politique",
        "source": "BBC"
    }
    ```
    """
    if not request.text or len(request.text) < 10:
        raise HTTPException(
            status_code=400,
            detail="Le texte doit contenir au moins 10 caractères"
        )

    try:
        result = model_loader.predict(request.text)
        
        if result.get("error"):
            raise HTTPException(
                status_code=500,
                detail=f"Erreur du modèle: {result['error']}"
            )
        
        return {
            "prediction": result["prediction"],
            "confidence_score": result["confidence_score"],
            "is_fake": result["is_fake"],
            "probabilities": result.get("probabilities"),
            "model_name": result["model_name"],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Erreur prédiction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict/batch")
async def predict_batch(texts: List[str]):
    """
    Prédit pour plusieurs textes en batch.
    Utile pour analyser plusieurs articles rapidement.
    """
    if not texts or len(texts) == 0:
        raise HTTPException(
            status_code=400,
            detail="Fournir au moins un texte"
        )
    
    if len(texts) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 textes par requête"
        )

    try:
        results = model_loader.predict_batch(texts)
        return {
            "count": len(results),
            "results": results,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Erreur prédiction batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINTS ARTICLES
# ─────────────────────────────────────────────

@app.get("/api/articles/real", response_model=dict)
async def get_real_articles(limit: int = 20, skip: int = 0):
    """
    Récupère les articles identifiés comme REAL (vrais).
    ✅ À afficher au frontend
    
    Paramètres:
        limit: Nombre d'articles à retourner (max 100)
        skip: Nombre d'articles à sauter (pagination)
    """
    if limit > 100:
        limit = 100
    
    try:
        articles = db_manager.get_real_articles(limit=limit, skip=skip)
        return {
            "count": len(articles),
            "articles": articles,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erreur récupération articles real: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/fake", response_model=dict)
async def get_fake_articles(limit: int = 20, skip: int = 0):
    """
    Récupère les articles identifiés comme FAKE (faux).
    ⚠️ Pour modération/audit
    """
    if limit > 100:
        limit = 100
    
    try:
        articles = db_manager.get_fake_articles(limit=limit, skip=skip)
        return {
            "count": len(articles),
            "articles": articles,
            "status": "success",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erreur récupération articles fake: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/all")
async def get_all_articles(limit: int = 20, skip: int = 0):
    """Récupère tous les articles (real + fake)."""
    if limit > 100:
        limit = 100
    
    try:
        articles = db_manager.get_all_articles(limit=limit, skip=skip)
        return {
            "count": len(articles),
            "articles": articles,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erreur récupération tous les articles: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/articles/by-category/{category}")
async def get_articles_by_category(category: str, limit: int = 20):
    """Récupère les articles par catégorie."""
    try:
        articles = db_manager.get_by_category(category, limit=limit)
        return {
            "category": category,
            "count": len(articles),
            "articles": articles,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erreur récupération par catégorie: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINTS STATISTIQUES
# ─────────────────────────────────────────────

@app.get("/api/stats", response_model=dict)
async def get_stats():
    """Récupère les statistiques globales de la base."""
    try:
        stats = db_manager.get_stats()
        
        total = stats["total"]
        real_count = stats["real"]
        fake_count = stats["fake"]
        unanalyzed = stats["unanalyzed"]
        
        return {
            "total_articles": total,
            "real": {
                "count": real_count,
                "percentage": (real_count / total * 100) if total > 0 else 0
            },
            "fake": {
                "count": fake_count,
                "percentage": (fake_count / total * 100) if total > 0 else 0
            },
            "unanalyzed": {
                "count": unanalyzed,
                "percentage": (unanalyzed / total * 100) if total > 0 else 0
            },
            "model_info": model_loader.get_model_info(),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Erreur récupération stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINTS COLLECTE/ENTRAÎNEMENT
# ─────────────────────────────────────────────

@app.post("/api/collect/once")
async def collect_once(background_tasks: BackgroundTasks):
    """
    Lance une collecte unique d'articles.
    Exécution en arrière-plan.
    """
    try:
        background_tasks.add_task(run_collection_job)
        return {
            "status": "Collecte lancée en arrière-plan",
            "message": "Les articles seront collectés et analysés"
        }
    except Exception as e:
        logger.error(f"Erreur démarrage collecte: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze/unanalyzed")
async def analyze_unanalyzed(limit: int = 50, background_tasks: BackgroundTasks = None):
    """
    Analyse les articles sans prédiction IA.
    """
    try:
        background_tasks.add_task(
            fake_news_connector.process_unanalyzed,
            limit=limit
        )
        return {
            "status": "Analyse lancée",
            "message": f"Jusqu'à {limit} articles seront analysés en arrière-plan"
        }
    except Exception as e:
        logger.error(f"Erreur analyse: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ─────────────────────────────────────────────
# ENDPOINTS SANTÉ
# ─────────────────────────────────────────────

@app.get("/api/health")
async def health_check():
    """Vérification santé de l'API."""
    model_ready = model_loader.is_ready()
    db_ready = db_manager is not None
    
    return {
        "status": "healthy" if (model_ready and db_ready) else "degraded",
        "model": "ready" if model_ready else "not_ready",
        "database": "ready" if db_ready else "not_ready",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/model-info")
async def model_info():
    """Informations détaillées du modèle."""
    return {
        "model_info": model_loader.get_model_info(),
        "is_ready": model_loader.is_ready(),
        "timestamp": datetime.now().isoformat()
    }


# ─────────────────────────────────────────────
# TÂCHE D'ARRIÈRE-PLAN
# ─────────────────────────────────────────────

def run_collection_job():
    """Collecte et analyse les articles."""
    logger.info("🚀 Collecte lancée...")
    try:
        agent = NewsCollectorAgent()
        stats = agent.run_pipeline(DEFAULT_RSS_SOURCES)
        logger.info(f"✓ Collecte terminée: {stats}")
        
        # Analyser les nouveaux articles
        analyzed = fake_news_connector.process_unanalyzed(limit=100)
        logger.info(f"✓ Analyse IA: {analyzed} articles traités")
    except Exception as e:
        logger.error(f"✗ Erreur collecte: {e}")


# Note: ROOT ENDPOINT (/) is handled by StaticFiles mounting at the end of this file
# StaticFiles will serve index.html for the frontend SPA when html=True is set


# Mount static files (frontend dist) at the very end, after all routes are defined
# This allows the catch-all to serve index.html for the SPA while preserving API routes
if FRONTEND_DIST and os.path.isdir(FRONTEND_DIST):
    try:
        app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
        logger.info(f"✓ Frontend mounted at /: {FRONTEND_DIST}")
    except Exception as e:
        logger.warning(f"⚠ Could not mount frontend: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
