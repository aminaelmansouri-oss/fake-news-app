"""
Exemple d'intégration Frontend - Comment utiliser l'API dans une application web.
Compatible React, Vue, Angular, ou JavaScript vanilla.
"""

# ====================================================================
# 1. EXEMPLE JAVASCRIPT / FETCH API (Vanilla JS)
# ====================================================================

javascript_example = """
// frontend/src/api.js

const API_URL = 'http://localhost:8000/api';

/**
 * Récupère les vraies news pour affichage
 */
export const fetchRealNews = async (limit = 20, skip = 0) => {
  try {
    const response = await fetch(
      `${API_URL}/articles/real?limit=${limit}&skip=${skip}`
    );
    const data = await response.json();
    return data.articles || [];
  } catch (error) {
    console.error('Erreur récupération real news:', error);
    return [];
  }
};

/**
 * Récupère les statistiques
 */
export const fetchStats = async () => {
  try {
    const response = await fetch(`${API_URL}/stats`);
    const data = await response.json();
    return {
      totalArticles: data.total_articles,
      real: data.real.count,
      realPercentage: data.real.percentage,
      fake: data.fake.count,
      fakePercentage: data.fake.percentage
    };
  } catch (error) {
    console.error('Erreur stats:', error);
    return null;
  }
};

/**
 * Prédit si un article est fake
 */
export const predictArticle = async (text, title = '') => {
  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, title })
    });
    const data = await response.json();
    return {
      prediction: data.prediction,
      confidence: (data.confidence_score * 100).toFixed(1),
      isFake: data.is_fake
    };
  } catch (error) {
    console.error('Erreur prédiction:', error);
    return null;
  }
};
"""

# ====================================================================
# 2. EXEMPLE REACT COMPONENT
# ====================================================================

react_example = """
// frontend/src/components/NewsBoard.jsx

import React, { useEffect, useState } from 'react';
import { fetchRealNews, fetchStats } from '../api';

export function NewsBoard() {
  const [articles, setArticles] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Charger les données
    const loadData = async () => {
      setLoading(true);
      
      // Récupérer vraies news
      const news = await fetchRealNews(20);
      setArticles(news);
      
      // Récupérer stats
      const statsData = await fetchStats();
      setStats(statsData);
      
      setLoading(false);
    };

    loadData();
    
    // Rafraîchir toutes les 5 minutes
    const interval = setInterval(loadData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading) return <div>Chargement...</div>;

  return (
    <div className="news-board">
      {/* En-tête avec statistiques */}
      <header className="header">
        <h1>📰 Tableau des News Vérifiées</h1>
        
        {stats && (
          <div className="stats">
            <div className="stat-box green">
              <h3>✅ Vraies News</h3>
              <p className="number">{stats.real}</p>
              <p className="percentage">{stats.realPercentage.toFixed(1)}%</p>
            </div>
            
            <div className="stat-box red">
              <h3>❌ Fausses News</h3>
              <p className="number">{stats.fake}</p>
              <p className="percentage">{stats.fakePercentage.toFixed(1)}%</p>
            </div>
            
            <div className="stat-box blue">
              <h3>📊 Total</h3>
              <p className="number">{stats.totalArticles}</p>
            </div>
          </div>
        )}
      </header>

      {/* Grille d'articles */}
      <main className="articles-grid">
        {articles.map((article, idx) => (
          <article key={idx} className="article-card">
            {/* Badge de confiance */}
            <div className="confidence-badge">
              🎯 {(article.score * 100).toFixed(1)}%
            </div>
            
            {/* Contenu */}
            <div className="article-header">
              <h2>{article.title}</h2>
              <p className="source">📌 {article.source}</p>
            </div>
            
            <div className="article-footer">
              <span className="date">
                📅 {new Date(article.published_at).toLocaleDateString('fr-FR')}
              </span>
              <span className="prediction">
                ✅ ARTICLE VÉRIFIÉ
              </span>
            </div>
            
            {/* Lien */}
            <a href={article.url} target="_blank" rel="noopener noreferrer" 
               className="article-link">
              Lire l'article complet →
            </a>
          </article>
        ))}
      </main>
    </div>
  );
}

// Styles CSS
const styles = `
.news-board {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
}

.header {
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  margin-bottom: 30px;
  color: #1a1a1a;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-box {
  padding: 20px;
  border-radius: 10px;
  color: white;
  text-align: center;
}

.stat-box.green {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.stat-box.red {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.stat-box.blue {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.stat-box .number {
  font-size: 2.5em;
  font-weight: bold;
  margin: 10px 0;
}

.stat-box .percentage {
  font-size: 0.9em;
  opacity: 0.9;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.article-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
  border-left: 5px solid #667eea;
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}

.confidence-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: #667eea;
  color: white;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85em;
  font-weight: bold;
}

.article-header h2 {
  font-size: 1.3em;
  margin: 0 0 10px 0;
  color: #1a1a1a;
  line-height: 1.4;
}

.source {
  color: #667eea;
  font-size: 0.9em;
  margin: 10px 0;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 15px 0;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.date {
  color: #999;
  font-size: 0.85em;
}

.prediction {
  background: #4caf50;
  color: white;
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 0.8em;
  font-weight: bold;
}

.article-link {
  display: inline-block;
  color: #667eea;
  text-decoration: none;
  font-weight: bold;
  margin-top: 10px;
  transition: color 0.3s;
}

.article-link:hover {
  color: #764ba2;
}
`;
"""

# ====================================================================
# 3. EXEMPLE VUE.JS 3 COMPONENT
# ====================================================================

vue_example = """
<!-- frontend/src/components/NewsBoard.vue -->

<template>
  <div class="news-board">
    <!-- Entête -->
    <header class="header">
      <h1>📰 Tableau des News Vérifiées</h1>
      
      <div class="stats" v-if="stats">
        <div class="stat-box green">
          <h3>✅ Vraies News</h3>
          <p class="number">{{ stats.real }}</p>
          <p class="percentage">{{ (stats.realPercentage).toFixed(1) }}%</p>
        </div>
        
        <div class="stat-box red">
          <h3>❌ Fausses News</h3>
          <p class="number">{{ stats.fake }}</p>
          <p class="percentage">{{ (stats.fakePercentage).toFixed(1) }}%</p>
        </div>
        
        <div class="stat-box blue">
          <h3>📊 Total</h3>
          <p class="number">{{ stats.totalArticles }}</p>
        </div>
      </div>
    </header>

    <!-- Grille articles -->
    <main class="articles-grid">
      <article 
        v-for="(article, idx) in articles" 
        :key="idx"
        class="article-card"
      >
        <div class="confidence-badge">
          🎯 {{ (article.score * 100).toFixed(1) }}%
        </div>
        
        <div class="article-header">
          <h2>{{ article.title }}</h2>
          <p class="source">📌 {{ article.source }}</p>
        </div>
        
        <div class="article-footer">
          <span class="date">
            📅 {{ formatDate(article.published_at) }}
          </span>
          <span class="prediction">✅ ARTICLE VÉRIFIÉ</span>
        </div>
        
        <a :href="article.url" target="_blank" class="article-link">
          Lire l'article complet →
        </a>
      </article>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const articles = ref([]);
const stats = ref(null);

const fetchRealNews = async (limit = 20) => {
  const response = await fetch(
    `http://localhost:8000/api/articles/real?limit=${limit}`
  );
  const data = await response.json();
  return data.articles || [];
};

const fetchStats = async () => {
  const response = await fetch('http://localhost:8000/api/stats');
  const data = await response.json();
  return {
    totalArticles: data.total_articles,
    real: data.real.count,
    realPercentage: data.real.percentage,
    fake: data.fake.count,
    fakePercentage: data.fake.percentage
  };
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('fr-FR');
};

const loadData = async () => {
  articles.value = await fetchRealNews(20);
  stats.value = await fetchStats();
};

onMounted(() => {
  loadData();
  setInterval(loadData, 5 * 60 * 1000); // Rafraîchir toutes les 5 min
});
</script>

<style scoped>
/* Même CSS que React */
.news-board { /* ... */ }
</style>
"""

# ====================================================================
# 4. EXEMPLE HTML PUR
# ====================================================================

html_example = """
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>📰 Tableau des News Vérifiées</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
      background: #f5f5f5;
      padding: 20px;
    }
    
    .container {
      max-width: 1400px;
      margin: 0 auto;
    }
    
    h1 {
      margin-bottom: 30px;
      color: #1a1a1a;
    }
    
    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    
    .stat-box {
      padding: 20px;
      border-radius: 10px;
      color: white;
      text-align: center;
    }
    
    .stat-box.real {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .stat-box.fake {
      background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .stat-box.total {
      background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .stat-box .number {
      font-size: 2.5em;
      font-weight: bold;
      margin: 10px 0;
    }
    
    .articles-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 20px;
    }
    
    .article-card {
      background: white;
      border-radius: 10px;
      padding: 20px;
      border-left: 5px solid #667eea;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
      transition: transform 0.3s;
    }
    
    .article-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .article-title {
      font-size: 1.2em;
      margin-bottom: 10px;
      color: #1a1a1a;
    }
    
    .article-source {
      color: #667eea;
      font-size: 0.9em;
    }
    
    .article-footer {
      display: flex;
      justify-content: space-between;
      margin-top: 15px;
      padding-top: 15px;
      border-top: 1px solid #eee;
      font-size: 0.85em;
    }
    
    .article-date {
      color: #999;
    }
    
    .article-badge {
      background: #4caf50;
      color: white;
      padding: 5px 10px;
      border-radius: 5px;
      font-weight: bold;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>📰 Tableau des News Vérifiées</h1>
    
    <div id="stats" class="stats"></div>
    <div id="articles" class="articles-grid"></div>
  </div>

  <script>
    const API_URL = 'http://localhost:8000/api';

    // Récupérer et afficher les stats
    async function loadStats() {
      const response = await fetch(`${API_URL}/stats`);
      const data = await response.json();
      
      const statsHtml = `
        <div class="stat-box real">
          <h3>✅ Vraies News</h3>
          <p class="number">${data.real.count}</p>
          <p>${data.real.percentage.toFixed(1)}%</p>
        </div>
        <div class="stat-box fake">
          <h3>❌ Fausses News</h3>
          <p class="number">${data.fake.count}</p>
          <p>${data.fake.percentage.toFixed(1)}%</p>
        </div>
        <div class="stat-box total">
          <h3>📊 Total</h3>
          <p class="number">${data.total_articles}</p>
        </div>
      `;
      
      document.getElementById('stats').innerHTML = statsHtml;
    }

    // Récupérer et afficher les articles
    async function loadArticles() {
      const response = await fetch(`${API_URL}/articles/real?limit=20`);
      const data = await response.json();
      
      const articlesHtml = data.articles.map(article => `
        <div class="article-card">
          <h2 class="article-title">${article.title}</h2>
          <p class="article-source">📌 ${article.source}</p>
          
          <div class="article-footer">
            <span class="article-date">📅 ${new Date(article.published_at).toLocaleDateString('fr-FR')}</span>
            <span class="article-badge">✅ VÉRIFIÉ</span>
          </div>
          
          <a href="${article.url}" target="_blank" style="color: #667eea; margin-top: 10px; display: block;">
            Lire l'article complet →
          </a>
        </div>
      `).join('');
      
      document.getElementById('articles').innerHTML = articlesHtml;
    }

    // Charger les données
    loadStats();
    loadArticles();

    // Rafraîchir toutes les 5 minutes
    setInterval(() => {
      loadStats();
      loadArticles();
    }, 5 * 60 * 1000);
  </script>
</body>
</html>
"""

# ====================================================================
# EXEMPLES DE REQUÊTES
# ====================================================================

requests_examples = """
## Requêtes CURL / Postman

### 1. Prédiction Simple
curl -X POST "http://localhost:8000/api/predict" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "The president announced new trade policies today",
    "title": "Breaking News"
  }'

Réponse:
{
  "prediction": "real",
  "confidence_score": 0.94,
  "is_fake": false,
  "model_name": "Stacking Classifier (TF-IDF)"
}

### 2. Récupérer les Vraies News
curl "http://localhost:8000/api/articles/real?limit=10&skip=0"

Réponse:
{
  "count": 10,
  "articles": [
    {
      "id": 1,
      "title": "Economic growth surges",
      "source": "Reuters",
      "prediction": "real",
      "score": 0.97
    },
    ...
  ]
}

### 3. Statistiques
curl "http://localhost:8000/api/stats"

Réponse:
{
  "total_articles": 5420,
  "real": {
    "count": 3850,
    "percentage": 71.0
  },
  "fake": {
    "count": 1570,
    "percentage": 29.0
  }
}

### 4. Batch Prédictions
curl -X POST "http://localhost:8000/api/predict/batch" \\
  -H "Content-Type: application/json" \\
  -d '[
    "First article text here",
    "Second article text here",
    "Third article text here"
  ]'
"""

if __name__ == "__main__":
    print("=== EXEMPLES D'INTÉGRATION FRONTEND ===\n")
    print("1. JavaScript Vanilla\n")
    print(javascript_example)
    print("\n2. React Component\n")
    print(react_example)
    print("\n3. Vue.js Component\n")
    print(vue_example)
    print("\n4. HTML Pur\n")
    print(html_example)
    print("\n5. Exemples Requêtes\n")
    print(requests_examples)
