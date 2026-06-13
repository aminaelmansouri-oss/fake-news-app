# Commandes Rapides - Fake News Detection System

## 🚀 Démarrage

### 1. Première exécution (setup complet)
```bash
# Se placer dans le répertoire
cd fake_news_agent

# Installer les dépendances
pip install -r requirements.txt

# Vérifier le modèle
python test_model_integration.py

# Lancer l'API
python launcher_api.py
```

### 2. Lancer l'API directement (après setup)
```bash
python launcher_api.py
```

### 3. Lancer l'API en mode développement
```bash
python -m uvicorn api:app --reload --port 8000
```

---

## 📝 Tests

### Tester l'intégration complète
```bash
python test_model_integration.py
```

### Test avec curl - Prédiction simple
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Breaking news about climate change", "title": "Climate Report"}'
```

### Test avec curl - Récupérer vraies news
```bash
curl "http://localhost:8000/api/articles/real?limit=20"
```

### Test avec curl - Stats
```bash
curl "http://localhost:8000/api/stats"
```

### Test avec curl - Health check
```bash
curl "http://localhost:8000/api/health"
```

---

## 🔍 Debugging

### Vérifier que le modèle charge
```bash
python -c "from agent.model_loader import get_model_loader; loader = get_model_loader(); print('✓ OK' if loader.is_ready() else '✗ ERREUR')"
```

### Vérifier les fichiers du modèle
```bash
ls -lh fake_news_models/
```

### Afficher les logs détaillés
```bash
python launcher_api.py 2>&1 | grep -E "ERROR|WARNING|INFO"
```

### Réinitialiser la base de données
```bash
rm fake_news_agent.db
# Elle sera recréée au prochain lancement
```

---

## 🌐 Accès API

| Ressource | URL |
|-----------|-----|
| **Swagger UI** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |
| **Health Check** | http://localhost:8000/api/health |
| **Real News** | http://localhost:8000/api/articles/real |
| **Fake News** | http://localhost:8000/api/articles/fake |
| **Predict** | http://localhost:8000/api/predict (POST) |

---

## 📊 Fichiers Clés

```
fake_news_agent/
├── fake_news_models/
│   └── stacking_classifier_tfidf.pkl    ← Modèle ML
├── agent/
│   ├── model_loader.py                  ← Charge modèle
│   ├── ai_connector.py                  ← Utilise modèle
│   └── database.py                      ← Persiste données
├── api.py                               ← API FastAPI
├── launcher_api.py                      ← Lance l'API
├── test_model_integration.py            ← Tests
├── requirements.txt                     ← Dépendances
└── INTEGRATION_README.md                ← Documentation
```

---

## 🔧 Configuration Rapide

### Changer le port API
```bash
# Dans launcher_api.py ligne ~130:
# subprocess.run([..., "--port", "8001", ...])

# Ou directement:
python -m uvicorn api:app --port 8001
```

### Activer la collecte automatique
```python
# Dans config/settings.py:
SCHEDULER_ENABLED = True
COLLECTION_INTERVAL_HOURS = 1
```

### Modifier les sources RSS
```python
# Dans config/settings.py:
DEFAULT_RSS_SOURCES = [
    "https://your-rss-feed.com/feed",
    # Ajouter plus de sources...
]
```

---

## 📈 Performance

| Action | Temps |
|--------|-------|
| Charger modèle | ~1s |
| Prédiction simple | ~2.5ms |
| Prédiction batch (100) | ~200ms |
| Lancer API | ~3s |
| Query base (20 articles) | ~50ms |

---

## ✅ Checklist Pré-Production

- [ ] Tous les tests passent (`python test_model_integration.py`)
- [ ] API répond sur http://localhost:8000/api/health
- [ ] Documentation API accessible sur http://localhost:8000/docs
- [ ] Base de données créée et remplie
- [ ] Frontend peut faire requêtes GET sur /api/articles/real
- [ ] CORS configuré correctement
- [ ] Logs en place et monitored
- [ ] Backups du modèle effectués

---

## 🚨 Erreurs Courantes et Solutions

| Erreur | Cause | Solution |
|--------|-------|----------|
| ModuleNotFoundError | Dépendances manquantes | `pip install -r requirements.txt` |
| Model not found | Fichiers modèle manquants | Exécuter Section 10 du notebook |
| Port already in use | Port 8000 utilisé | Changer le port ou tuer le processus |
| Database locked | Connexion active | Arrêter autres processus, supprimer .db |
| CORS error (frontend) | CORS pas configuré | Vérifier api.py ligne ~30 |

---

## 📞 Support Rapide

```bash
# Vérifier tout en une commande
python test_model_integration.py && echo "✅ Système OK"

# Tester modèle uniquement
python -c "from agent.model_loader import get_model_loader; loader = get_model_loader(); print(loader.predict('test'))"

# Afficher version Python
python --version

# Afficher packages installés
pip list | grep -E "scikit|fastapi|joblib"
```

---

## 🎯 Points d'Intégration Frontend

### React/Vue
```javascript
const API_URL = 'http://localhost:8000';

// Récupérer vraies news
const response = await fetch(`${API_URL}/api/articles/real?limit=20`);
const news = await response.json();
```

### HTML Vanilla
```html
<script>
async function loadNews() {
  const response = await fetch('http://localhost:8000/api/articles/real?limit=20');
  const data = await response.json();
  // Afficher data.items
}
loadNews();
</script>
```

---

**Prêt? Lancez `python launcher_api.py` et débutez!** 🚀
