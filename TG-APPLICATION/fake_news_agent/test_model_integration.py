#!/usr/bin/env python3
"""
Test d'intégration du modèle Stacking + TF-IDF avec le système complet.
Vérifie que le modèle charge, prédit et s'intègre avec la base de données.
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin du projet
sys.path.insert(0, str(Path(__file__).parent))

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_1_model_loader():
    """Test 1: Vérifier que le modèle charge correctement"""
    print("\n" + "="*80)
    print("TEST 1: Chargement du Modèle Stacking")
    print("="*80)
    
    try:
        from agent.model_loader import get_model_loader
        
        loader = get_model_loader()
        
        if not loader.is_ready():
            print("❌ ÉCHEC: Modèle non chargé")
            return False
            
        print("✅ SUCCÈS: Modèle Stacking chargé")
        print(f"   - Modèle: {loader.model.__class__.__name__}")
        print(f"   - Vectorizer: {loader.vectorizer.__class__.__name__}")
        print(f"   - Métadonnées: {'Oui' if loader.metadata else 'Non'}")
        
        if loader.metadata:
            print(f"   - Test Accuracy: {loader.metadata.get('test_set_metrics', {}).get('accuracy', 'N/A')}")
            print(f"   - Test F1: {loader.metadata.get('test_set_metrics', {}).get('f1_score', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_2_simple_prediction():
    """Test 2: Faire une prédiction simple"""
    print("\n" + "="*80)
    print("TEST 2: Prédiction Simple")
    print("="*80)
    
    try:
        from agent.model_loader import get_model_loader
        
        loader = get_model_loader()
        
        # Article fake sample
        fake_text = """
        Trump Claims He Was Wiretapped By Obama During Campaign
        President Trump claimed without evidence that he was wiretapped 
        by the Obama administration during the 2016 campaign.
        """
        
        # Article real sample
        real_text = """
        Federal Reserve Raises Interest Rates by 0.25%
        The Federal Reserve announced today that it is raising the federal 
        funds rate by 0.25 percentage points to combat inflation.
        """
        
        print("\n📄 Test 1 - Article potentiellement FAKE:")
        print(f"   Texte: {fake_text[:60]}...")
        result_fake = loader.predict(fake_text)
        print(f"   ✓ Prédiction: {result_fake['prediction'].upper()}")
        print(f"   ✓ Confiance: {result_fake['confidence_score']*100:.1f}%")
        
        print("\n📄 Test 2 - Article potentiellement REAL:")
        print(f"   Texte: {real_text[:60]}...")
        result_real = loader.predict(real_text)
        print(f"   ✓ Prédiction: {result_real['prediction'].upper()}")
        print(f"   ✓ Confiance: {result_real['confidence_score']*100:.1f}%")
        
        if result_fake['prediction'] in ['fake', 'real'] and result_real['prediction'] in ['fake', 'real']:
            print("\n✅ SUCCÈS: Prédictions effectuées")
            return True
        else:
            print("\n❌ ÉCHEC: Prédictions invalides")
            return False
            
    except Exception as e:
        print(f"❌ ÉCHEC: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_3_batch_prediction():
    """Test 3: Prédictions batch"""
    print("\n" + "="*80)
    print("TEST 3: Prédictions Batch")
    print("="*80)
    
    try:
        from agent.model_loader import get_model_loader
        
        loader = get_model_loader()
        
        texts = [
            "Breaking: Scientists discover new species in Amazon rainforest",
            "Fake news alert: Celebrity secretly replaced by clone",
            "Market report: Tech stocks rise 2% amid economic recovery"
        ]
        
        results = loader.predict_batch(texts)
        
        print(f"\n📊 Résultats pour {len(texts)} textes:")
        for i, (text, result) in enumerate(zip(texts, results), 1):
            print(f"\n   {i}. {text[:50]}...")
            print(f"      Prédiction: {result['prediction'].upper()}")
            print(f"      Confiance: {result['confidence_score']*100:.1f}%")
        
        if len(results) == len(texts):
            print(f"\n✅ SUCCÈS: {len(results)} prédictions batch")
            return True
        else:
            print(f"\n❌ ÉCHEC: Seulement {len(results)}/{len(texts)} prédictions")
            return False
            
    except Exception as e:
        print(f"❌ ÉCHEC: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_4_ai_connector():
    """Test 4: Test du connecteur AI avec la base de données"""
    print("\n" + "="*80)
    print("TEST 4: Connecteur AI + Base de Données")
    print("="*80)
    
    try:
        from models.article import Article
        from agent.ai_connector import FakeNewsConnector
        
        connector = FakeNewsConnector()
        
        # Créer un article test
        article = Article(
            title="Test Article - Fake News Detection",
            content="This is a test article for fake news detection model integration.",
            url="http://test-url.com",
            source="test-source"
        )
        
        # Prédire
        result = connector.predict(article)
        
        print(f"\n📰 Article: {article.title}")
        print(f"   URL: {article.url}")
        print(f"   ✓ Prédiction: {result['prediction'].upper() if result['prediction'] else 'ERREUR'}")
        print(f"   ✓ Confiance: {result['confidence_score']*100:.1f}%" if result['confidence_score'] else "   ✓ Confiance: N/A")
        
        if result['prediction'] in ['real', 'fake']:
            print(f"\n✅ SUCCÈS: Intégration AI Connector fonctionnelle")
            return True
        else:
            print(f"\n❌ ÉCHEC: Prédiction invalide")
            return False
            
    except Exception as e:
        print(f"❌ ÉCHEC: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_5_model_info():
    """Test 5: Récupérer les informations du modèle"""
    print("\n" + "="*80)
    print("TEST 5: Informations du Modèle")
    print("="*80)
    
    try:
        from agent.model_loader import get_model_loader
        
        loader = get_model_loader()
        info = loader.get_model_info()
        
        print(f"\n📋 Informations du Modèle:")
        print(f"   - Nom: {info.get('model_name', 'N/A')}")
        print(f"   - Type: {info.get('model_type', 'N/A')}")
        print(f"   - Date: {info.get('training_date', 'N/A')}")
        
        if info.get('test_metrics'):
            metrics = info['test_metrics']
            print(f"\n   📊 Métriques Test:")
            print(f"      - Accuracy: {metrics.get('accuracy', 'N/A')}")
            print(f"      - F1 Score: {metrics.get('f1_score', 'N/A')}")
            print(f"      - ROC AUC: {metrics.get('roc_auc', 'N/A')}")
        
        if info.get('base_learners'):
            print(f"\n   🔧 Base Learners ({len(info['base_learners'])}):")
            for bl in info['base_learners']:
                print(f"      - {bl}")
        
        print(f"\n✅ SUCCÈS: Informations du modèle récupérées")
        return True
        
    except Exception as e:
        print(f"❌ ÉCHEC: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Exécuter tous les tests"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "TESTS D'INTÉGRATION - MODÈLE STACKING + TF-IDF".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")
    
    tests = [
        ("Chargement du modèle", test_1_model_loader),
        ("Prédiction simple", test_2_simple_prediction),
        ("Prédictions batch", test_3_batch_prediction),
        ("Connecteur AI", test_4_ai_connector),
        ("Informations modèle", test_5_model_info),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Erreur lors de l'exécution de {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "="*80)
    print("RÉSUMÉ DES TESTS")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ SUCCÈS" if result else "❌ ÉCHEC"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests réussis")
    
    if passed == total:
        print("\n🎉 TOUS LES TESTS RÉUSSIS! Le système est opérationnel.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) échoué(s). Vérifiez les erreurs ci-dessus.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
