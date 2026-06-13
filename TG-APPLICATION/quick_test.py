#!/usr/bin/env python3
"""
Quick test script to verify the API is working correctly.
Run this after starting the API server to validate endpoints.
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
TIMEOUT = 5

def print_header(text: str):
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}")

def print_result(name: str, success: bool, message: str = ""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"  {status} - {name}")
    if message:
        print(f"         {message}")

def test_health():
    """Test /api/health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            is_healthy = data.get("status") == "healthy"
            model_ready = data.get("model") == "ready"
            print_result("Health Check", is_healthy and model_ready, f"Status: {data.get('status')}")
            return is_healthy and model_ready
    except Exception as e:
        print_result("Health Check", False, str(e))
    return False

def test_model_info():
    """Test /api/model-info endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/model-info", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            print_result("Model Info", True, f"Model: {data.get('model_info', {}).get('model_name', 'Unknown')}")
            return True
    except Exception as e:
        print_result("Model Info", False, str(e))
    return False

def test_single_prediction():
    """Test /api/predict endpoint"""
    try:
        payload = {
            "text": "Breaking news: Scientists discover new treatment for disease. The research team at the university has conducted extensive studies...",
            "title": "Medical Breakthrough",
            "source": "Science Daily"
        }
        response = requests.post(f"{BASE_URL}/api/predict", json=payload, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            prediction = data.get("prediction")
            confidence = data.get("confidence_score", 0)
            print_result(
                "Single Prediction",
                prediction in ["real", "fake"],
                f"Prediction: {prediction} (Confidence: {confidence:.2%})"
            )
            return True
    except Exception as e:
        print_result("Single Prediction", False, str(e))
    return False

def test_batch_prediction():
    """Test /api/predict/batch endpoint"""
    try:
        texts = [
            "The president announced a new policy today",
            "Scientists find cure for common cold",
            "Local community organizes charity event"
        ]
        response = requests.post(f"{BASE_URL}/api/predict/batch", json=texts, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)
            print_result("Batch Prediction", count == len(texts), f"Processed: {count} articles")
            return count == len(texts)
    except Exception as e:
        print_result("Batch Prediction", False, str(e))
    return False

def test_get_articles():
    """Test /api/articles/* endpoints"""
    try:
        # Test real articles
        response = requests.get(f"{BASE_URL}/api/articles/real?limit=5", timeout=TIMEOUT)
        real_ok = response.status_code == 200
        real_count = 0
        if real_ok:
            real_count = response.json().get("count", 0)
        
        # Test fake articles
        response = requests.get(f"{BASE_URL}/api/articles/fake?limit=5", timeout=TIMEOUT)
        fake_ok = response.status_code == 200
        fake_count = 0
        if fake_ok:
            fake_count = response.json().get("count", 0)
        
        # Test all articles
        response = requests.get(f"{BASE_URL}/api/articles/all?limit=5", timeout=TIMEOUT)
        all_ok = response.status_code == 200
        all_count = 0
        if all_ok:
            all_count = response.json().get("count", 0)
        
        print_result("Get Articles (real)", real_ok, f"Found: {real_count} articles")
        print_result("Get Articles (fake)", fake_ok, f"Found: {fake_count} articles")
        print_result("Get Articles (all)", all_ok, f"Found: {all_count} articles")
        
        return real_ok and fake_ok and all_ok
    except Exception as e:
        print_result("Get Articles", False, str(e))
    return False

def test_statistics():
    """Test /api/stats endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            total = data.get("total_articles", 0)
            real = data.get("real", {}).get("count", 0)
            fake = data.get("fake", {}).get("count", 0)
            print_result(
                "Statistics",
                True,
                f"Total: {total}, Real: {real}, Fake: {fake}"
            )
            return True
    except Exception as e:
        print_result("Statistics", False, str(e))
    return False

def test_frontend():
    """Test that frontend is served at root"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        if response.status_code == 200:
            is_html = "<!DOCTYPE" in response.text or "<html" in response.text or ".js" in response.text
            print_result("Frontend SPA", is_html, "HTML/JS content served at root")
            return is_html
    except Exception as e:
        print_result("Frontend SPA", False, str(e))
    return False

def test_swagger_ui():
    """Test that Swagger UI is available"""
    try:
        response = requests.get(f"{BASE_URL}/docs", timeout=TIMEOUT)
        if response.status_code == 200:
            is_swagger = "swagger" in response.text.lower() or "openapi" in response.text.lower()
            print_result("Swagger UI", is_swagger, "Documentation available at /docs")
            return is_swagger
    except Exception as e:
        print_result("Swagger UI", False, str(e))
    return False

def main():
    """Run all tests"""
    print_header("🚀 FAKE NEWS DETECTION API - QUICK TEST")
    print(f"\nTesting API at: {BASE_URL}")
    print(f"Timeout: {TIMEOUT} seconds\n")
    
    tests = [
        ("Core Functionality", [
            test_health,
            test_model_info,
        ]),
        ("Predictions", [
            test_single_prediction,
            test_batch_prediction,
        ]),
        ("Data Retrieval", [
            test_get_articles,
            test_statistics,
        ]),
        ("Frontend & Docs", [
            test_frontend,
            test_swagger_ui,
        ]),
    ]
    
    total_tests = 0
    passed_tests = 0
    
    for category, test_funcs in tests:
        print(f"\n{category}:")
        for test_func in test_funcs:
            total_tests += 1
            try:
                result = test_func()
                if result:
                    passed_tests += 1
            except Exception as e:
                print_result(test_func.__name__, False, str(e))
    
    # Summary
    print_header("📊 TEST SUMMARY")
    print(f"\n  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests} ✅")
    print(f"  Failed: {total_tests - passed_tests} ❌")
    
    percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    print(f"  Success Rate: {percentage:.1f}%\n")
    
    if passed_tests == total_tests:
        print_header("✨ ALL TESTS PASSED - SYSTEM IS READY! ✨")
    else:
        print_header("⚠️  SOME TESTS FAILED - CHECK LOGS ABOVE")
    
    return 0 if passed_tests == total_tests else 1

if __name__ == "__main__":
    import sys
    print("\nNote: Ensure the API server is running on http://localhost:8000")
    print("Command: python -m uvicorn api:app --host 0.0.0.0 --port 8000\n")
    
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user")
        sys.exit(1)
