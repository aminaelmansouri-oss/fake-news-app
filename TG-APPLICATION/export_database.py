#!/usr/bin/env python3
"""
Script pour exporter la base de données SQLite en différents formats.
Usage:
    python export_database.py          # Exporte en CSV (par défaut)
    python export_database.py csv      # Exporte en CSV
    python export_database.py json     # Exporte en JSON
    python export_database.py excel    # Exporte en Excel
"""

import os
import sys
import sqlite3
import json
import csv
from pathlib import Path
from datetime import datetime

# Déterminer le chemin de la base de données
BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "fake_news_agent.db"

def export_to_csv(output_file=None):
    """Exporte la base de données en fichiers CSV"""
    if not DB_PATH.exists():
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    if output_file is None:
        output_dir = BASE_DIR / "exports"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"articles_{timestamp}.csv"
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Récupérer la structure des tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Exporting database: {DB_PATH}")
        print(f"📁 Tables trouvées: {len(tables)}")
        
        # Exporter chaque table
        for (table_name,) in tables:
            print(f"\n  Exporting table: {table_name}")
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            if not rows:
                print(f"    ⚠️  Table vide")
                continue
            
            # Récupérer les noms des colonnes
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Exporter en CSV
            csv_file = output_dir / f"{table_name}_{timestamp}.csv"
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
            
            print(f"    ✓ Exporté: {csv_file.name} ({len(rows)} lignes)")
        
        conn.close()
        print(f"\n✅ Export CSV terminé!")
        print(f"📁 Fichiers dans: {output_dir}")
        return output_dir
    
    except Exception as e:
        print(f"❌ Erreur lors de l'export CSV: {e}")
        return None

def export_to_json(output_file=None):
    """Exporte la base de données en JSON"""
    if not DB_PATH.exists():
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    if output_file is None:
        output_dir = BASE_DIR / "exports"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"database_{timestamp}.json"
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        data = {}
        print(f"📊 Exporting database to JSON: {output_file}")
        
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            data[table_name] = [dict(row) for row in rows]
            print(f"  ✓ {table_name}: {len(rows)} records")
        
        # Sérialiser en JSON avec support pour les dates
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        
        conn.close()
        print(f"\n✅ Export JSON terminé!")
        print(f"📁 Fichier: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"❌ Erreur lors de l'export JSON: {e}")
        return None

def export_to_excel(output_file=None):
    """Exporte la base de données en Excel"""
    try:
        import openpyxl
        from openpyxl.styles import PatternFill, Font, Alignment
    except ImportError:
        print("⚠️  openpyxl non installé. Exécutez: pip install openpyxl")
        return None
    
    if not DB_PATH.exists():
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    if output_file is None:
        output_dir = BASE_DIR / "exports"
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"database_{timestamp}.xlsx"
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Créer un workbook
        wb = openpyxl.Workbook()
        wb.remove(wb.active)  # Supprimer la feuille par défaut
        
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 Exporting database to Excel: {output_file}")
        
        for (table_name,) in tables:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # Récupérer les noms des colonnes
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            # Créer une feuille pour cette table
            ws = wb.create_sheet(title=table_name[:31])  # Excel: max 31 caractères
            
            # Ajouter l'en-tête
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_font = Font(color="FFFFFF", bold=True)
            
            for col_idx, col_name in enumerate(columns, 1):
                cell = ws.cell(row=1, column=col_idx, value=col_name)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")
            
            # Ajouter les données
            for row_idx, row in enumerate(rows, 2):
                for col_idx, value in enumerate(row, 1):
                    ws.cell(row=row_idx, column=col_idx, value=value)
            
            # Auto-ajuster les colonnes
            for col in ws.columns:
                max_length = 0
                column_letter = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            print(f"  ✓ {table_name}: {len(rows)} records")
        
        # Sauvegarder le workbook
        wb.save(output_file)
        conn.close()
        
        print(f"\n✅ Export Excel terminé!")
        print(f"📁 Fichier: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"❌ Erreur lors de l'export Excel: {e}")
        return None

def copy_database_file(output_dir=None):
    """Copie le fichier database.db original"""
    if not DB_PATH.exists():
        print(f"❌ Base de données non trouvée: {DB_PATH}")
        return
    
    if output_dir is None:
        output_dir = BASE_DIR / "exports"
        output_dir.mkdir(exist_ok=True)
    
    try:
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = output_dir / f"fake_news_agent_{timestamp}.db"
        shutil.copy2(str(DB_PATH), str(output_file))
        
        # Afficher la taille
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"✅ Base de données copiée!")
        print(f"📁 Fichier: {output_file}")
        print(f"📊 Taille: {size_mb:.2f} MB")
        return output_file
    
    except Exception as e:
        print(f"❌ Erreur lors de la copie: {e}")
        return None

def main():
    """Fonction principale"""
    format_type = sys.argv[1].lower() if len(sys.argv) > 1 else "csv"
    
    print("=" * 60)
    print("🗄️  DATABASE EXPORT TOOL")
    print("=" * 60)
    
    if format_type == "csv":
        export_to_csv()
    elif format_type == "json":
        export_to_json()
    elif format_type == "excel" or format_type == "xlsx":
        export_to_excel()
    elif format_type == "copy":
        output_dir = Path(__file__).parent / "exports"
        output_dir.mkdir(exist_ok=True)
        copy_database_file(output_dir)
    else:
        print(f"❌ Format inconnu: {format_type}")
        print("\nFormats supportés:")
        print("  csv     - Exporte chaque table en CSV")
        print("  json    - Exporte toute la base en JSON")
        print("  excel   - Exporte toute la base en Excel")
        print("  copy    - Copie le fichier .db original")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
