#!/usr/bin/env python3
"""
Script pour insérer des données de test dans la base de données
"""
import sys
import os
from pathlib import Path

# Ajouter les chemins
current_dir = Path(__file__).parent.absolute()
parent_dir = current_dir.parent.absolute()
sys.path.insert(0, str(current_dir))
os.chdir(str(current_dir))

from datetime import datetime
from agent.database import DatabaseManager

# Données de test
TEST_ARTICLES = [
    {
        "title": "Climate scientists warn of unprecedented Arctic ice melt",
        "content": "New research from Arctic institutes shows record ice loss. Scientists warn this could accelerate global warming significantly.",
        "source": "Reuters",
        "url": "https://reuters.com/article1",
        "prediction": "real",
        "confidence_score": 0.95
    },
    {
        "title": "Government to replace all currency with microchips by 2027",
        "content": "This is completely false. No government has announced such a plan. This appears to be misinformation.",
        "source": "Anonymous Blog",
        "url": "https://conspiracynews.net/article",
        "prediction": "fake",
        "confidence_score": 0.92
    },
    {
        "title": "New vaccine shows promise in early trials",
        "content": "Early clinical trials show positive results but more testing is needed. Scientists remain cautious about timeline.",
        "source": "Medical Journal",
        "url": "https://sciencedirect.com/article",
        "prediction": "mixed",
        "confidence_score": 0.68
    },
    {
        "title": "Tech giant announces major data breach affecting millions",
        "content": "Security researchers confirm the breach. Company issues apology and offers credit monitoring.",
        "source": "TechCrunch",
        "url": "https://techcrunch.com/article",
        "prediction": "real",
        "confidence_score": 0.98
    },
    {
        "title": "Celebrity death hoax spreads on social media",
        "content": "Popular actor is alive and well. Rumor started from parody account and spread quickly.",
        "source": "Twitter",
        "url": "https://twitter.com/article",
        "prediction": "fake",
        "confidence_score": 0.89
    },
    {
        "title": "Economic indicators suggest potential market correction",
        "content": "Financial experts are divided on interpretation. Some see warning signs, others expect stability.",
        "source": "Financial Times",
        "url": "https://ft.com/article",
        "prediction": "mixed",
        "confidence_score": 0.55
    },
]

def main():
    print("=" * 60)
    print("Insertion de donnees de test dans la base de donnees")
    print("=" * 60)
    
    try:
        db = DatabaseManager()
        print("\n[DB] Connexion established")
        
        print(f"\nInsertion de {len(TEST_ARTICLES)} articles...")
        
        for i, article in enumerate(TEST_ARTICLES, 1):
            try:
                db.insert_article(
                    title=article["title"],
                    content=article["content"],
                    source=article["source"],
                    url=article["url"],
                    prediction=article["prediction"],
                    confidence_score=article["confidence_score"]
                )
                print(f"  [{i}/{len(TEST_ARTICLES)}] OK - {article['title'][:50]}...")
            except Exception as e:
                print(f"  [{i}/{len(TEST_ARTICLES)}] ERROR - {str(e)}")
        
        print("\n✓ Insertion terminee!")
        
        # Verification
        print("\nVerification de la base de donnees:")
        stats = db.get_stats()
        print(f"  Total articles: {stats['total']}")
        print(f"  Real: {stats['real']}")
        print(f"  Fake: {stats['fake']}")
        print(f"  Unanalyzed: {stats['unanalyzed']}")
        
        print("\n✓ Succes!")
        return True
    
    except Exception as e:
        print(f"\nERREUR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()
