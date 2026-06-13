# 🤖 Agent Collecteur de News — Robot Journaliste Intelligent

Composant autonome de collecte, nettoyage et structuration des actualités
pour alimenter une plateforme de **détection de Fake News** et de **journal personnalisé**.

---

## 🏗️ Architecture du projet

```
fake_news_agent/
│
├── main.py                    # Point d'entrée
│
├── agent/
│   ├── collector.py           # Collecte RSS + Scraping web
│   ├── database.py            # Gestion SQLite / PostgreSQL
│   └── ai_connector.py        # Connecteur vers le modèle Fake News
│
├── config/
│   └── settings.py            # Configuration centrale (sources, DB, IA)
│
├── models/
│   └── article.py             # Modèle de données Article
│
├── utils/
│   ├── cleaner.py             # Nettoyage & normalisation du texte
│   ├── deduplicator.py        # Détection des doublons
│   └── source_checker.py      # Vérification de la crédibilité des sources
│
├── scheduler/
│   └── scheduler.py           # Planificateur automatique (APScheduler)
│
├── tests/
│   └── test_agent.py          # Tests unitaires (pytest)
│
└── requirements.txt           # Dépendances Python
```

---

## ⚙️ Pipeline de collecte

```
Sites de News / RSS Feeds
         ↓
  Agent Collecteur
         ↓
  Nettoyage & Structuration
         ↓
  Déduplication
         ↓
  Vérification des Sources
         ↓
  Base de Données SQLite
         ↓
  Modèle IA Fake News
         ↓
  Backend API
         ↓
  Journal Personnalisé Utilisateur
```

---

## 🚀 Installation

```bash
# 1. Cloner le projet
git clone https://github.com/votre-repo/fake-news-agent.git
cd fake_news_agent

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate   # Windows : venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

---

## ▶️ Utilisation

```bash
# Lancer le scheduler automatique (collecte toutes les heures)
python main.py

# Lancer une collecte unique et quitter
python main.py --once

# Afficher les statistiques de la base
python main.py --stats

# Lancer les tests unitaires
pytest tests/ -v
```

---

## 📰 Sources collectées par défaut

| Source      | Type | URL                                      |
|-------------|------|------------------------------------------|
| BBC         | RSS  | feeds.bbci.co.uk/news/rss.xml           |
| Reuters     | RSS  | feeds.reuters.com/reuters/topNews        |
| CNN         | RSS  | rss.cnn.com/rss/edition.rss             |
| Al Jazeera  | RSS  | aljazeera.com/xml/rss/all.xml           |
| DW          | RSS  | rss.dw.com/rdf/rss-en-all               |

> Ajoutez vos sources dans `config/settings.py` → `DEFAULT_RSS_SOURCES`

---

## 🧠 Format de données Article

```json
{
  "title": "France wins the World Cup",
  "content": "France defeated Argentina in a thrilling final...",
  "source": "BBC",
  "author": "John Smith",
  "url": "https://bbc.com/sport/article/123",
  "category": "Sports",
  "published_at": "2024-12-18T22:30:00",
  "prediction": "real",
  "confidence_score": 0.94,
  "collected_at": "2024-12-18T23:00:00"
}
```

---

## 🔧 Configuration (`config/settings.py`)

| Paramètre                  | Défaut        | Description                          |
|----------------------------|---------------|--------------------------------------|
| `TRUSTED_SOURCES`          | BBC, Reuters… | Whitelist des sources fiables        |
| `SCHEDULER_INTERVAL_HOURS` | `1`           | Fréquence de collecte (heures)       |
| `SIMILARITY_THRESHOLD`     | `0.85`        | Seuil de similarité anti-doublons    |
| `DATABASE_URL`             | SQLite local  | URL de connexion base de données     |
| `FAKE_NEWS_MODEL_ENDPOINT` | localhost:8000| URL du modèle IA Fake News           |

---

## 🧪 Tests

```bash
pytest tests/ -v --cov=. --cov-report=term-missing
```

Couvre : `TextCleaner`, `Deduplicator`, `SourceChecker`, `Article`

---

## 📄 Licence

MIT License — Projet académique / Recherche en détection de désinformation.
