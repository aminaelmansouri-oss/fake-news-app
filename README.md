#  TruthGuard — Plateforme de Détection des Fake News par IA

Plateforme web intelligente de détection automatique des fake news par Intelligence Artificielle et Machine Learning.

---

## Architecture

```
truthguard/
├── backend/                  # Flask API + Modèle IA
│   ├── app.py                # Point d'entrée Flask
│   ├── config.py             # Configuration
│   ├── requirements.txt
│   │
│   ├── model/
│   │   ├── train_model.py    # Script d'entraînement
│   │   ├── fake_news_model.pkl   # Modèle Logistic Regression (généré)
│   │   ├── vectorizer_word.pkl   # TF-IDF word-level (généré)
│   │   └── vectorizer_char.pkl   # TF-IDF char-level (généré)
│   │
│   ├── scraper/
│   │   └── scraper.py        # Scraping BeautifulSoup
│   ├── preprocessing/
│   │   └── clean_text.py     # Pipeline NLP (NLTK)
│   ├── routes/
│   │   └── predict_routes.py # Endpoints REST
│   ├── services/
│   │   └── prediction_service.py
│   ├── database/
│   │   └── db.py             # SQLite (historique)
│   └── datasets/
│       ├── fake.csv          # (à placer manuellement — ISOT)
│       └── true.csv
│
└── frontend/                 # Interface HTML/CSS/JS
    ├── index.html            # Page principale (analyse)
    ├── pages/
    │   ├── dashboard.html    # Statistiques & visualisations
    │   ├── history.html      # Historique des analyses
    │   └── about.html        # Documentation technique
    ├── css/
    │   ├── style.css
    │   └── dashboard.css
    └── js/
        ├── api.js            # Client API REST
        ├── app.js            # Logique principale
        └── dashboard.js      # Dashboard charts
```

---

## Démarrage rapide

### 1. Lancer le backend

```bash
# Option A — Script automatique
chmod +x start.sh && ./start.sh

# Option B — Manuel
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python model/train_model.py   # entraîne le modèle (1ère fois)
python app.py                 # démarre l'API sur :5000
```

### 2. Ouvrir le frontend

Ouvrez `frontend/index.html` dans votre navigateur.  
Avec Live Server (VS Code) sur le port 5500, CORS est déjà configuré.

---

## API REST

| Endpoint | Méthode | Description |
|---|---|---|
| `GET /api/health` | GET | Statut de l'API |
| `POST /api/predict/text` | POST | Analyser un texte |
| `POST /api/predict/url` | POST | Analyser une URL |
| `GET /api/history` | GET | Historique des analyses |
| `GET /api/stats` | GET | Statistiques agrégées |

### Exemples

```bash
# Analyser un texte
curl -X POST http://localhost:5000/api/predict/text \
  -H "Content-Type: application/json" \
  -d '{"text": "Scientists discover new cancer treatment with 95% success rate in clinical trials"}'

# Analyser une URL
curl -X POST http://localhost:5000/api/predict/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.bbc.com/news/article-example"}'
```

### Réponse

```json
{
  "prediction": "REAL",
  "confidence": 0.9231,
  "confidence_label": "High",
  "confidence_pct": 92.3,
  "fake_score": 0.0769,
  "real_score": 0.9231,
  "fake_pct": 7.7,
  "real_pct": 92.3,
  "word_count": 124
}
```

---

## Modèle IA

Le modèle suit le pipeline du notebook **TruthGuard_Complet_version_finale.ipynb** :

| Composant | Détail |
|---|---|
| Prétraitement | NLTK : lowercase → URLs/HTML → tokenisation → stopwords → POS lemmatisation |
| Vectorisation | TF-IDF word (1-2 grams, 10k) + char_wb (3-5 grams, 5k) concaténés |
| Modèle | Logistic Regression (class_weight=balanced, C=1.0) |
| Split | Stratifié 80/20, seed=42 |
| Accuracy | ~97% sur dataset ISOT (avec fake.csv + true.csv) |

### Dataset

Placez les fichiers CSV dans `backend/datasets/` :
- `fake.csv` — Articles fake (ISOT dataset)
- `true.csv` — Articles réels (ISOT dataset)

Sans les CSV, le script génère un mini dataset de démonstration.

---

## Technologies

**Backend :** Python, Flask, scikit-learn, NLTK, BeautifulSoup4, SQLite  
**Frontend :** HTML5, CSS3 (variables, grid, animations), Vanilla JS, Fetch API, SVG natif
