
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
* react js (Frontend)

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

##  Dataset

Le modèle est entraîné sur un dataset de fake news contenant :

* texte des articles
* label (Fake / Real)

---



##  Conclusion

Ce projet combine le Machine Learning et le développement web pour proposer une solution simple de détection des fake news, contribuant à lutter contre la désinformation.

---

