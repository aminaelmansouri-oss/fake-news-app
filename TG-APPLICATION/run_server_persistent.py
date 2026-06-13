#!/usr/bin/env python3
"""
Script pour lancer le serveur FastAPI en mode persistant
"""
import os
import sys
import signal
import time

# Chemin vers le répertoire de l'app
script_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(script_dir, "fake_news_agent")

os.chdir(app_dir)
sys.path.insert(0, app_dir)

def main():
    import uvicorn
    
    print("\n" + "="*60)
    print("FAKE NEWS DETECTION API - STARTING")
    print("="*60)
    print(f"Working directory: {os.getcwd()}")
    print(f"Server: http://0.0.0.0:8000")
    print(f"API Docs: http://localhost:8000/docs")
    print(f"Frontend: http://localhost:8000/")
    print("="*60)
    print("Press CTRL+C to stop the server\n")
    
    try:
        # Run the server
        uvicorn.run(
            "api:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
