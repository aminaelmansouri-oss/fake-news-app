#!/usr/bin/env python3
"""
Launcher automatisé pour le système Fake News Detection.
Vérifie les dépendances, le modèle, et lance l'API FastAPI.
"""

import os
import sys
import subprocess
from pathlib import Path

# Couleurs pour l'affichage
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header():
    """Affiche le header"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "FAKE NEWS DETECTION - LAUNCHER".center(78) + "║")
    print("║" + "Stacking Classifier + TF-IDF".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝\n")


def check_python_version():
    """Vérifie la version Python"""
    print(f"{BLUE}[1/5] Vérification Python...{RESET}")
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"{GREEN}✓ Python {version.major}.{version.minor}.{version.micro}{RESET}\n")
        return True
    else:
        print(f"{RED}✗ Python 3.8+ requis (actuellement {version.major}.{version.minor}){RESET}\n")
        return False


def check_dependencies():
    """Vérifie les dépendances Python"""
    print(f"{BLUE}[2/5] Vérification des dépendances...{RESET}")
    
    required_packages = [
        'sklearn',
        'fastapi',
        'uvicorn',
        'joblib',
        'numpy',
        'pandas',
        'nltk',
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"  {GREEN}✓{RESET} {package}")
        except ImportError:
            print(f"  {RED}✗{RESET} {package}")
            missing.append(package)
    
    if missing:
        print(f"\n{RED}Packages manquants: {', '.join(missing)}{RESET}")
        print(f"{YELLOW}Exécutez: pip install -r requirements.txt{RESET}\n")
        return False
    else:
        print(f"{GREEN}✓ Toutes les dépendances OK{RESET}\n")
        return True


def check_model_files():
    """Vérifie la présence des fichiers du modèle"""
    print(f"{BLUE}[3/5] Vérification des fichiers du modèle...{RESET}")
    
    model_dir = Path("fake_news_models")
    
    if not model_dir.exists():
        print(f"{RED}✗ Dossier 'fake_news_models' non trouvé{RESET}")
        print(f"{YELLOW}Exécutez d'abord la Section 10 du notebook ISOT_FAKENEWS_NB.ipynb{RESET}\n")
        return False
    
    required_files = [
        "stacking_classifier_tfidf.pkl",
        "stacking_classifier_tfidf.joblib",
        "tfidf_vectorizer.pkl",
        "tfidf_vectorizer.joblib",
        "model_metadata.json"
    ]
    
    missing_files = []
    for filename in required_files:
        filepath = model_dir / filename
        if filepath.exists():
            size_mb = filepath.stat().st_size / (1024*1024)
            print(f"  {GREEN}✓{RESET} {filename} ({size_mb:.2f} MB)")
        else:
            print(f"  {RED}✗{RESET} {filename}")
            missing_files.append(filename)
    
    if missing_files:
        print(f"\n{RED}Fichiers manquants: {', '.join(missing_files)}{RESET}\n")
        return False
    else:
        print(f"{GREEN}✓ Tous les fichiers du modèle présents{RESET}\n")
        return True


def test_model_loading():
    """Test le chargement du modèle"""
    print(f"{BLUE}[4/5] Test du chargement du modèle...{RESET}")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from agent.model_loader import get_model_loader
        
        loader = get_model_loader()
        
        if not loader.is_ready():
            print(f"{RED}✗ Modèle non chargé correctement{RESET}\n")
            return False
        
        print(f"  {GREEN}✓{RESET} Modèle Stacking chargé")
        print(f"  {GREEN}✓{RESET} Vectorizer TF-IDF chargé")
        
        # Test simple prediction
        test_text = "This is a test article for fake news detection"
        result = loader.predict(test_text)
        
        if result.get('prediction') in ['real', 'fake']:
            print(f"  {GREEN}✓{RESET} Prédiction test: {result['prediction'].upper()} ({result['confidence_score']*100:.1f}%)")
            print(f"{GREEN}✓ Modèle prêt{RESET}\n")
            return True
        else:
            print(f"{RED}✗ Prédiction invalide{RESET}\n")
            return False
            
    except Exception as e:
        print(f"{RED}✗ Erreur lors du test du modèle: {e}{RESET}\n")
        return False


def start_api():
    """Lance l'API FastAPI"""
    print(f"{BLUE}[5/5] Démarrage de l'API...{RESET}\n")
    
    try:
        print(f"{BOLD}API lancée sur: http://localhost:8000{RESET}")
        print(f"{BOLD}Documentation: http://localhost:8000/docs{RESET}")
        print(f"{BOLD}ReDoc: http://localhost:8000/redoc{RESET}")
        print(f"\n{YELLOW}Appuyez sur Ctrl+C pour arrêter l'API{RESET}\n")
        
        # Lancer uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "api:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print(f"\n{YELLOW}API arrêtée{RESET}\n")
    except Exception as e:
        print(f"{RED}✗ Erreur lors du lancement: {e}{RESET}\n")
        return False
    
    return True


def main():
    """Fonction principale"""
    print_header()
    
    # Checks
    checks = [
        ("Version Python", check_python_version),
        ("Dépendances", check_dependencies),
        ("Fichiers modèle", check_model_files),
        ("Chargement modèle", test_model_loading),
    ]
    
    for check_name, check_func in checks:
        if not check_func():
            print(f"\n{RED}✗ Vérification échouée: {check_name}{RESET}")
            print(f"{YELLOW}Impossible de lancer l'API{RESET}\n")
            return 1
    
    # Summary
    print("="*80)
    print(f"{GREEN}✓ TOUS LES CHECKS RÉUSSIS{RESET}")
    print("="*80 + "\n")
    
    # Start API
    start_api()
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
