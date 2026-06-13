#!/usr/bin/env python3
import sqlite3
import csv
from pathlib import Path
from datetime import datetime

db_file = "fake_news_agent.db"
export_dir = Path("../exports")
export_dir.mkdir(exist_ok=True)

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print(f"Tables found: {len(tables)}")
for table_name, in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  - {table_name}: {count} rows")

# Export articles
cursor.execute("SELECT * FROM articles")
rows = cursor.fetchall()

if rows:
    cursor.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in cursor.fetchall()]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_file = export_dir / f"articles_{timestamp}.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    
    print(f"\nExported: {csv_file.name} ({len(rows)} rows)")
else:
    print("No articles to export")

conn.close()
