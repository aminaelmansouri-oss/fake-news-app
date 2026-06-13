╔════════════════════════════════════════════════════════════════════════════════╗
║                                                                                ║
║            ✅ HOW TO START THE FAKE NEWS DETECTION APPLICATION ✅              ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝

## 🚀 Quick Start (2 minutes)

### Option 1: Using Python (Recommended)

```powershell
# 1. Open PowerShell and navigate to project root
cd "c:\Users\hp\OneDrive\M1-IAOC-S2\Technique d'IA\fake_news_agent"

# 2. Run the startup script
.\.venv\Scripts\python.exe start_api.py
```

**You should see:**
```
============================================================
🚀 FAKE NEWS DETECTION API
============================================================
📁 Working directory: ...\fake_news_agent\fake_news_agent
🌐 Server: http://0.0.0.0:8000
📖 API Docs: http://localhost:8000/docs
🏠 Frontend: http://localhost:8000/
============================================================
Press CTRL+C to stop the server

INFO:agent.database:[DB] Base de données initialisée.
INFO:agent.model_loader:✓ Modèle Stacking chargé
INFO:agent.model_loader:✓ Vectorizer TF-IDF chargé
...
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Option 2: Direct Command (If Option 1 fails)

```powershell
# Navigate to the fake_news_agent subdirectory
cd "c:\Users\hp\OneDrive\M1-IAOC-S2\Technique d'IA\fake_news_agent\fake_news_agent"

# Run uvicorn directly
..\.venv\Scripts\python.exe -m uvicorn api:app --host 0.0.0.0 --port 8000
```

---

## 🌐 Access the Application

Once the server is running, open your browser and visit:

### Main Interface
```
http://localhost:8000/
```
**What you'll see:**
- Frontend React application
- Navigation menu with tabs:
  - 🏠 Home
  - ✅ Real News
  - ❌ Fake News
  - 📊 Statistics
  - ℹ️ Model Info

### API Documentation (Interactive)
```
http://localhost:8000/docs
```
**Swagger UI with all API endpoints**
- Test endpoints directly
- See request/response examples
- View all available parameters

### Alternative API Docs (ReDoc)
```
http://localhost:8000/redoc
```
**Different documentation format (ReDoc)**

### Health Check
```
http://localhost:8000/api/health
```
**JSON Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "model": "loaded",
  "api_version": "1.0.0"
}
```

---

## 📊 Available API Endpoints

### Article Retrieval

**Get Real Articles**
```
GET http://localhost:8000/api/articles/real?limit=20&skip=0
```

**Get Fake Articles**
```
GET http://localhost:8000/api/articles/fake?limit=20&skip=0
```

**Get Statistics**
```
GET http://localhost:8000/api/stats
```

**Get Model Information**
```
GET http://localhost:8000/api/model-info
```

---

## 🛑 Stop the Server

**In the terminal where the server is running, press:**
```
CTRL + C
```

You should see:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
```

---

## ⚙️ Server Configuration

### Current Setup
- **Host:** 0.0.0.0 (accessible from any machine on network)
- **Port:** 8000
- **Reload:** Disabled (for stability)
- **Workers:** 1

### To Change Settings
Edit `start_api.py` and modify the `uvicorn.run()` parameters:

```python
uvicorn.run(
    "api:app",
    host="127.0.0.1",  # Change here (127.0.0.1 = localhost only)
    port=8000,         # Change port here
    reload=False       # Set to True for auto-reload on code changes
)
```

---

## 🐛 Troubleshooting

### Issue: "Port 8000 already in use"
```powershell
# Find what's using port 8000
Get-NetTCPConnection -LocalPort 8000 | Select-Object OwningProcess

# Kill the process (replace XXXX with PID)
Stop-Process -Id XXXX -Force
```

### Issue: "Module not found" error
```powershell
# Make sure you're in the correct directory
cd "c:\Users\hp\OneDrive\M1-IAOC-S2\Technique d'IA\fake_news_agent"

# Make sure .venv exists
if (Test-Path .\.venv) { Write-Host "Virtual environment OK" } else { Write-Host "Need to recreate .venv" }
```

### Issue: "Python not found"
```powershell
# Check Python is installed
.\.venv\Scripts\python.exe --version

# Should show: Python 3.13.x
```

### Issue: Model not loading
```powershell
# Check if model files exist
Test-Path ".\fake_news_models\stacking_classifier_tfidf.pkl"
Test-Path ".\fake_news_models\tfidf_vectorizer.pkl"
```

---

## 📋 System Requirements

- ✅ Windows 10/11
- ✅ Python 3.13.5 (in .venv)
- ✅ 500 MB disk space
- ✅ 4 GB RAM minimum
- ✅ Internet connection (for initial setup only)

---

## 📁 Project Structure for Reference

```
fake_news_agent/
├── fake_news_agent/           # Main application code
│   ├── api.py                 # FastAPI application
│   ├── agent/                 # AI and database modules
│   ├── config/                # Configuration
│   └── models/                # Data models
├── frontend/                  # React UI
│   └── dist/                  # Built frontend (served by API)
├── fake_news_models/          # ML model files
│   ├── stacking_classifier_tfidf.pkl
│   ├── tfidf_vectorizer.pkl
│   └── model_metadata.json
├── .venv/                     # Virtual environment
├── start_api.py               # Server startup script (USE THIS!)
├── requirements.txt           # Dependencies
└── fake_news_agent.db         # SQLite database
```

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Start Server | `.\.venv\Scripts\python.exe start_api.py` |
| Stop Server | `CTRL + C` in terminal |
| Access UI | Open `http://localhost:8000/` |
| View Docs | Open `http://localhost:8000/docs` |
| Check Health | Visit `http://localhost:8000/api/health` |
| View Logs | Check terminal output |

---

## ✅ Success Indicators

When the server starts successfully, you should see:

1. ✅ `[DB] Base de données initialisée` (Database initialized)
2. ✅ `✓ Modèle Stacking chargé` (Stacking model loaded)
3. ✅ `✓ Vectorizer TF-IDF chargé` (TF-IDF vectorizer loaded)
4. ✅ `✓ Frontend mounted at /` (Frontend mounted)
5. ✅ `Uvicorn running on http://0.0.0.0:8000` (Server running)

---

## 🎓 Next Steps

1. **Explore the Frontend**
   - Go to http://localhost:8000/
   - Browse Real News vs Fake News
   - Check statistics

2. **Test the API**
   - Go to http://localhost:8000/docs
   - Try different endpoints
   - See real predictions

3. **Add New Articles**
   - The system collects articles from RSS feeds
   - Check the database for predictions
   - Monitor accuracy

---

**🎉 You're all set! The application is ready to use!**

For detailed documentation, see:
- `README_FINAL.md` - Full documentation
- `QUICK_START.md` - Quick reference
- `PRODUCTION_READY_GUIDE.md` - Deployment guide
