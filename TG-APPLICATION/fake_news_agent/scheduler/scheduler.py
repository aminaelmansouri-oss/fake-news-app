"""
Planificateur automatique de collecte.
Lance le pipeline de collecte toutes les X heures via APScheduler.
"""

import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from agent.collector import NewsCollectorAgent
from agent.ai_connector import FakeNewsConnector
from config.settings import DEFAULT_RSS_SOURCES, SCHEDULER_INTERVAL_HOURS

logger = logging.getLogger(__name__)


def run_collection_job():
    """Tâche principale exécutée à intervalles réguliers."""
    logger.info("═" * 60)
    logger.info("  LANCEMENT DU JOB DE COLLECTE AUTOMATIQUE")
    logger.info("═" * 60)

    # 1. Collecte & nettoyage & stockage
    agent = NewsCollectorAgent()
    stats = agent.run_pipeline(DEFAULT_RSS_SOURCES)
    logger.info(f"Collecte terminée : {stats}")

    # 2. Analyse IA des articles en attente
    connector = FakeNewsConnector()
    analyzed = connector.process_unanalyzed(limit=100)
    logger.info(f"Analyse IA terminée : {analyzed} articles traités")


def start_scheduler():
    """Démarre le planificateur en mode bloquant."""
    scheduler = BlockingScheduler()

    scheduler.add_job(
        run_collection_job,
        trigger=IntervalTrigger(hours=SCHEDULER_INTERVAL_HOURS),
        id="collect_news",
        name="Collecte automatique des news",
        replace_existing=True,
    )

    logger.info(
        f"Scheduler démarré — collecte toutes les {SCHEDULER_INTERVAL_HOURS}h"
    )

    # Exécution immédiate au démarrage
    run_collection_job()

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler arrêté manuellement.")
        scheduler.shutdown()
