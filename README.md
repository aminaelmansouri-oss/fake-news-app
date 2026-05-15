
#  Fake News Detection Web App

## Description

Ce projet consiste à développer une application web intelligente capable de détecter les fake news en utilisant des techniques de Machine Learning et de traitement du langage naturel (NLP).

L’utilisateur peut saisir un texte ou une actualité, et le système analyse automatiquement le contenu pour déterminer si l’information est **réelle (Real)** ou **fausse (Fake)**.

---

##  Objectifs

* Détecter automatiquement les fake news
* Utiliser des techniques de Machine Learning
* Créer une application web simple et fonctionnelle
* Connecter un modèle IA avec une interface utilisateur

---

##  Structure du projet

```
fake-news-app/
│
├── data/
│   └── dataset.csv
│
├── notebook/
│   └── model.ipynb
│
├── model/
│   ├── model.pkl
│   └── vectorizer.pkl
│
├── backend/
│   └── app.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── README.md
└── requirements.txt
```

---

## Technologies utilisées

### Machine Learning

* Python
* Scikit-learn
* Pandas
* TF-IDF

###  Web

* Flask (Backend)
* HTML / CSS / JavaScript (Frontend)

---

##  Fonctionnement

1. L’utilisateur entre un texte ou une news
2. Le frontend envoie la requête au backend
3. Le backend :

   * prétraite le texte
   * transforme le texte en vecteur (TF-IDF)
   * applique le modèle ML
4. Le système retourne :

   * Fake ou Real
5. Le résultat est affiché à l’utilisateur

---

##  Installation et exécution

### 1. Cloner le projet

```
git clone https://github.com/username/fake-news-app.git
cd fake-news-app
```

### 2. Installer les dépendances

```
pip install -r requirements.txt
```

### 3. Lancer le backend

```
cd backend
python app.py
```

### 4. Lancer le frontend

* Ouvrir le fichier `frontend/index.html` dans le navigateur

---

## Dataset ISOT

Le projet s’appuie sur le **ISOT Fake News Dataset**, qui regroupe des articles réels et falsifiés provenant de sources de presse. 
Chaque enregistrement contient notamment :

* **title** : titre de l’article
* **text** : contenu de l’article
* **subject** : thématique (politics, news, etc.)
* **date** : date de publication
* **label** : *real* ou *fake*

Ce dataset sert de base pour l’EDA, le nettoyage NLP, la vectorisation TF‑IDF et l’entraînement des modèles.

---

## Objectifs spécifiques (ISOT)

* Explorer et analyser la distribution des classes et des thèmes
* Nettoyer et normaliser les textes (URLs, HTML, ponctuation, lemmatisation)
* Vectoriser le corpus (TF‑IDF uni/bi‑grams)
* Comparer plusieurs modèles de classification (classiques et ensembles)
* Préparer les résultats pour une intégration web

---

## Répartition collective (alternance A→B→A→C→B)

### 1) **A (Aymane) – EDA + Description Dataset**

* Présentation ISOT (structure, colonnes, tailles)
* Analyse basique (longueurs, classes, graphiques simples)
* Conclusion EDA

### 2) **B (Fatima) – Nettoyage + NLP preprocessing**

* Nettoyage : minuscules, ponctuation, stopwords
* Tokenization, lemmatization
* Pipeline de prétraitement commun

### 3) **A (Aymane) – Vectorisation TF‑IDF**

* Construction TF‑IDF
* Matrices train/test
* Justification de TF‑IDF

### 4) **C (Hajar) – Modèles ML avec TF‑IDF (6 modèles)**

* Entraîner 6 modèles : SVM, Logistic, RF, XGBoost, LightGBM, Stacking
* Sauvegarder les résultats bruts (accuracy, F1, etc.)

### 5) **B (Fatima) – Vectorisation Word2Vec**

* Construire Word2Vec (pré‑entraîné ou entraîné sur corpus)
* Générer les vecteurs par document
* Préparation train/test

### 6) **A (Aymane) – Modèles ML avec Word2Vec (6 modèles)**

* Même 6 modèles
* Résultats bruts

### 7) **C (Hajar) – Tableau comparatif global**

* Tableau final : 6 modèles × 2 vectorisations
* Comparaison globale (accuracy, F1, etc.)
* Graphique optionnel

### 8) **B (Fatima) – Optimisation (GridSearch / CV)**

* Sur les meilleurs modèles (TF‑IDF + Word2Vec)
* Réévaluation

### 9) **A (Aymane) – Conclusion + Best Model**

* Résumé final
* Modèle choisi et justification
* Pistes d’amélioration

---



##  Conclusion

Ce projet combine le Machine Learning et le développement web pour proposer une solution simple de détection des fake news, contribuant à lutter contre la désinformation.

---

