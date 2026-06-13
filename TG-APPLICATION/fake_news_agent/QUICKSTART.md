# ⚡ Quick Start - Fake News Detection

## 3 Étapes pour Lancer le Système Complet

### ✅ Étape 1 : Générer le Modèle (5 minutes)

Ouvrir `ISOT_FAKENEWS_NB.ipynb` et exécuter la **Section 10** :

```python
# Section 10.1 - Implémentation du Stacking Classifier
# Section 10.2 - Évaluation du Stacking Classifier  
# Section 10.3 - Visualisations
# Section 10.4 - Sauvegarde du Modèle pour Production
```

**Résultat :** Dossier `fake_news_models/` créé avec 3 fichiers

---

### ✅ Étape 2 : Installer les Dépendances (2 minutes)

```bash
cd fake_news_agent
pip install -r requirements.txt
```

---

### ✅ Étape 3 : Démarrer l'API (1 minute)

**Option 1 : Launcher complet** (recommandé)
```bash
python launcher.py
```

**Option 2 : Démarrer manuellement**
```bash
python -m uvicorn api:app --reload --port 8000
```

**Résultat :**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✅ API prête à recevoir des requêtes
```

---

## 🧪 Tester Immédiatement

### Terminal 1 : API Running
```bash
python launcher.py
# → http://localhost:8000/docs
```

### Terminal 2 : Test Prédiction
```bash
curl -X POST "http://localhost:8000/api/predict" \
  -H "Content-Type: application/json" \
  -d '{"text":"The president announced new policies today"}'
```

**Réponse :**
```json
{
  "prediction": "real",
  "confidence_score": 0.94,
  "model_name": "Stacking Classifier (TF-IDF)"
}
```

---

## 🎨 Utiliser dans Frontend

### React / Vue.js

```javascript
// Récupérer les vraies news pour afficher
const response = await fetch('http://localhost:8000/api/articles/real?limit=10');
const data = await response.json();

// data.articles = [
//   { id: 1, title: "...", source: "Reuters", prediction: "real", score: 0.95 },
//   ...
// ]
```

---

## 📊 Endpoints Principaux

| Endpoint | Méthode | Usage |
|----------|---------|-------|
| `/api/articles/real` | GET | ✅ **AFFICHER au frontend** |
| `/api/articles/fake` | GET | ⚠️ Modération |
| `/api/stats` | GET | 📊 Dashboard |
| `/api/predict` | POST | 🔮 Analyser texte |
| `/docs` | Browser | 📚 Docs interactif |

---

## 🔧 Troubleshooting

| Problème | Solution |
|----------|----------|
| "ModuleNotFoundError: No module named 'mlxtend'" | `pip install mlxtend==0.23.0` |
| "Modèle non trouvé" | Exécuter Section 10 du notebook |
| "Port 8000 en use" | `python -m uvicorn api:app --port 8001` |
| "CORS error" | Frontend et API doivent être sur même origine |

---

## 📚 Documentation Complète

Voir : `GUIDE_INTEGRATION.md`

---

**C'est tout ! Le système est prêt pour la production.** 🚀
