#!/usr/bin/env python3
"""
Script pour collecter des articles et exporter en CSV
"""
import sys
import os
from pathlib import Path

# Ajouter le chemin correct
sys.path.insert(0, str(Path(__file__).parent))

def collect_articles():
    """Lancer la collecte d'articles"""
    print("=" * 60)
    print("🚀 LANCEMENT DE LA COLLECTE D'ARTICLES")
    print("=" * 60)
    
    try:
        from fake_news_agent.collector import NewsCollectorAgent
        from config.settings import DEFAULT_RSS_SOURCES
        
        print(f"\n📡 Sources RSS à collecter: {len(DEFAULT_RSS_SOURCES)}")
        for source in DEFAULT_RSS_SOURCES[:3]:
            print(f"   • {source}")
        if len(DEFAULT_RSS_SOURCES) > 3:
            print(f"   ... et {len(DEFAULT_RSS_SOURCES) - 3} autres sources")
        
        agent = NewsCollectorAgent()
        print("\n⏳ Collecte en cours (cela peut prendre 30-60 secondes)...")
        stats = agent.run_pipeline(DEFAULT_RSS_SOURCES)
        
        print(f"\n✅ Collecte terminée!")
        print(f"   Statistiques: {stats}")
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur lors de la collecte: {e}")
        import traceback
        traceback.print_exc()
        return False

def export_to_csv():
    """Exporter la base de données en CSV"""
    print("\n" + "=" * 60)
    print("📊 EXPORT EN CSV")
    print("=" * 60)
    
    try:
        import sqlite3
        import csv
        from datetime import datetime
        
        db_path = Path(__file__).parent / "fake_news_agent.db"
        if not db_path.exists():
            print(f"❌ Base de données non trouvée: {db_path}")
            return False
        
        export_dir = Path(__file__).parent / "exports"
        export_dir.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\n📁 Tables trouvées: {len(tables)}")
        
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print(f"   ⚠️  {table_name}: table vide")
                continue
            
            # Récupérer les noms des colonnes
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Exporter en CSV
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            csv_file = export_dir / f"{table_name}_{timestamp}.csv"
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
            
            print(f"   ✓ {table_name}: {len(rows)} lignes → {csv_file.name}")
        
        conn.close()
        print(f"\n✅ Export terminé!")
        print(f"📁 Fichiers dans: {export_dir}")
        return True
    
    except Exception as e:
        print(f"\n❌ Erreur lors de l'export: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Fonction principale"""
    # Étape 1: Collecter
    if not collect_articles():
        print("\n⚠️  Collecte échouée, mais on essaie quand même l'export...")
    
    # Étape 2: Exporter
    export_to_csv()
    
    print("\n" + "=" * 60)
    print("✨ TERMINÉ!")
    print("=" * 60)

if __name__ == "__main__":
    main()
