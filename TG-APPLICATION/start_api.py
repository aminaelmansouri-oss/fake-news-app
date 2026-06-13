#!/usr/bin/env python3
"""
Simple script to start the Fake News Detection API
Works from any directory!
"""
import os
import sys

# Move to the fake_news_agent subdirectory where the code lives
script_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.join(script_dir, "fake_news_agent")

os.chdir(app_dir)
sys.path.insert(0, app_dir)

# Now launch uvicorn
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("🚀 FAKE NEWS DETECTION API")
    print("="*60)
    print(f"📁 Working directory: {os.getcwd()}")
    print(f"🌐 Server: http://0.0.0.0:8000")
    print(f"📖 API Docs: http://localhost:8000/docs")
    print(f"🏠 Frontend: http://localhost:8000/")
    print("="*60)
    print("Press CTRL+C to stop the server\n")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
