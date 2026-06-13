"""
Point d'entrée principal de l'Agent Collecteur de News.

Utilisation :
    python main.py               → Lance le scheduler automatique
    python main.py --once        → Lance une collecte unique et quitte
    python main.py --stats       → Affiche les statistiques de la base
"""

import argparse
import logging
import sys
import os

# ─────────────────────────────────────────────
# CONFIGURATION DU LOGGING
# ─────────────────────────────────────────────
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/agent.log", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Agent Collecteur de News - Robot Journaliste Intelligent"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Lance une collecte unique sans scheduler",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Affiche les statistiques de la base de données",
    )
    args = parser.parse_args()

    # ─── Affichage des stats ───
    if args.stats:
        from agent.database import DatabaseManager
        db = DatabaseManager()
        stats = db.get_stats()
        print("\n📊 STATISTIQUES DE LA BASE DE DONNÉES")
        print("=" * 40)
        print(f"  Total articles   : {stats['total']}")
        print(f"  ✅  Vrais         : {stats['real']}")
        print(f"  ❌  Fakes         : {stats['fake']}")
        print(f"  ⏳  Non analysés  : {stats['unanalyzed']}")
        print("=" * 40)
        return

    # ─── Collecte unique ───
    if args.once:
        logger.info("MODE : collecte unique")
        from scheduler.scheduler import run_collection_job
        run_collection_job()
        return

    # ─── Mode scheduler (défaut) ───
    logger.info("MODE : scheduler automatique")
    from scheduler.scheduler import start_scheduler
    start_scheduler()


if __name__ == "__main__":
    main()
