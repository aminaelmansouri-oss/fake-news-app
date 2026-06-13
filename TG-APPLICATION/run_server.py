#!/usr/bin/env python3
"""
Script to run the Fake News Detection API server
Run from project root: python run_server.py
"""

import sys
import os

# Get project root
project_root = os.path.dirname(os.path.abspath(__file__))

# Change to the directory where api.py lives (for relative imports to work)
os.chdir(os.path.join(project_root, "fake_news_agent"))
sys.path.insert(0, os.path.join(project_root, "fake_news_agent"))

# Now import and run uvicorn
import uvicorn

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid issues
        log_level="info"
    )
