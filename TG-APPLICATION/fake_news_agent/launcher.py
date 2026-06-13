"""
Launcher complet pour la solution Fake News Detection.
Démarre tout en une commande.
"""

import subprocess
import sys
import time
import os
from pathlib import Path

# Couleurs pour l'output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """Affiche la bannière du projet."""
    print(f"""
{Colors.BOLD}{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🤖 FAKE NEWS DETECTION - STACKING + TF-IDF                ║
║                                                               ║
║   Mode Complet : Modèle IA + Database + API FastAPI         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
{Colors.END}
    """)


def check_dependencies():
    """Vérifie les dépendances Python."""
    print(f"\n{Colors.YELLOW}[1/4] Vérification des dépendances...{Colors.END}")
    
    required = {
        'sklearn': 'scikit-learn',
        'mlxtend': 'mlxtend',
        'fastapi': 'fastapi',
        'joblib': 'joblib',
    }
    
    missing = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  {Colors.GREEN}✓{Colors.END} {name}")
        except ImportError:
            print(f"  {Colors.RED}✗{Colors.END} {name} (manquant)")
            missing.append(name)
    
    if missing:
        print(f"\n{Colors.RED}❌ Dépendances manquantes :{Colors.END}")
        for pkg in missing:
            print(f"   pip install {pkg}")
        return False
    
    print(f"  {Colors.GREEN}✓ Toutes les dépendances OK{Colors.END}")
    return True


def check_model_files():
    """Vérifie si les fichiers du modèle existent."""
    print(f"\n{Colors.YELLOW}[2/4] Vérification du modèle...{Colors.END}")
    
    model_dir = Path("fake_news_models")
    required_files = [
        "stacking_classifier_tfidf.joblib",
        "tfidf_vectorizer.joblib",
        "model_metadata.json"
    ]
    
    if not model_dir.exists():
        print(f"  {Colors.RED}✗{Colors.END} Dossier 'fake_news_models' introuvable")
        print(f"\n{Colors.YELLOW}Solution :{Colors.END}")
        print("  1. Ouvrir le notebook : ISOT_FAKENEWS_NB.ipynb")
        print("  2. Exécuter les cellules de la Section 10 (Stacking Classifier)")
        print("  3. Exécuter la cellule 10.4 (Sauvegarde du modèle)")
        return False
    
    for file in required_files:
        file_path = model_dir / file
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"  {Colors.GREEN}✓{Colors.END} {file} ({size_mb:.1f}MB)")
        else:
            print(f"  {Colors.RED}✗{Colors.END} {file} (manquant)")
            return False
    
    print(f"  {Colors.GREEN}✓ Modèle OK{Colors.END}")
    return True


def test_model():
    """Teste le modèle en isolation."""
    print(f"\n{Colors.YELLOW}[3/4] Test du modèle...{Colors.END}")
    
    try:
        from agent.model_loader import get_model_loader
        
        loader = get_model_loader()
        if not loader.is_ready():
            print(f"  {Colors.RED}✗ Modèle non initialisé{Colors.END}")
            return False
        
        # Test de prédiction
        test_text = "Breaking news: Scientists discover new treatment"
        result = loader.predict(test_text)
        
        if "error" in result:
            print(f"  {Colors.RED}✗ Erreur prédiction: {result['error']}{Colors.END}")
            return False
        
        print(f"  {Colors.GREEN}✓ Prédiction test OK{Colors.END}")
        print(f"    Texte: '{test_text[:40]}...'")
        print(f"    Résultat: {result['prediction'].upper()} ({result['confidence_score']*100:.1f}%)")
        return True
        
    except Exception as e:
        print(f"  {Colors.RED}✗ Erreur: {e}{Colors.END}")
        return False


def start_api():
    """Lance l'API FastAPI."""
    print(f"\n{Colors.YELLOW}[4/4] Démarrage de l'API FastAPI...{Colors.END}\n")
    
    try:
        print(f"{Colors.CYAN}Lancement sur http://localhost:8000{Colors.END}\n")
        print(f"{Colors.BOLD}Documentation interactive :{Colors.END}")
        print(f"  🔵 Swagger UI  : http://localhost:8000/docs")
        print(f"  🟢 ReDoc       : http://localhost:8000/redoc")
        print(f"  🔴 API Root    : http://localhost:8000/\n")
        
        print(f"{Colors.BOLD}Endpoints principales :{Colors.END}")
        print(f"  ✅ GET /api/articles/real     → Vraies news (FRONTEND)")
        print(f"  ❌ GET /api/articles/fake     → Fausses news (AUDIT)")
        print(f"  📊 GET /api/stats             → Statistiques")
        print(f"  🔮 POST /api/predict          → Analyse")
        print(f"  ❤️  GET /api/health           → Santé API\n")
        
        print(f"{Colors.BOLD}Appuyez sur Ctrl+C pour arrêter{Colors.END}\n")
        
        # Démarrer uvicorn
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "api:app", "--reload", "--port", "8000"],
            cwd=str(Path(__file__).parent)
        )
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}API arrêtée{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}✗ Erreur démarrage API: {e}{Colors.END}")
        print(f"\n{Colors.YELLOW}Solution:{Colors.END}")
        print(f"  pip install fastapi uvicorn")


def main():
    """Programme principal."""
    print_banner()
    
    # Vérifications
    if not check_dependencies():
        sys.exit(1)
    
    if not check_model_files():
        sys.exit(1)
    
    if not test_model():
        sys.exit(1)
    
    # Démarrer l'API
    print(f"\n{Colors.GREEN}✅ Tous les checks passés !{Colors.END}")
    print(f"\n{Colors.BOLD}{Colors.CYAN}Démarrage du système...{Colors.END}")
    
    start_api()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Arrêt du programme{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Erreur: {e}{Colors.END}")
        sys.exit(1)
