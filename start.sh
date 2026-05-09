#!/usr/bin/env bash
# ═══════════════════════════════════════════════
#  TruthGuard — Quick Start Script
# ═══════════════════════════════════════════════

set -e

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║           TruthGuard — Setup              ║"
echo "║   Fake News Detection Platform            ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

BACKEND_DIR="$(cd "$(dirname "$0")/backend" && pwd)"
FRONTEND_DIR="$(cd "$(dirname "$0")/frontend" && pwd)"

# ─── 1. Virtual environment ─────────────────────
echo " Setting up Python environment..."
cd "$BACKEND_DIR"

if [ ! -d "venv" ]; then
  python3 -m venv venv
  echo "   Virtual environment created."
fi

source venv/bin/activate
echo "   Activated."

# ─── 2. Dependencies ─────────────────────────────
echo ""
echo " Installing dependencies..."
pip install -r requirements.txt -q
echo "   Done."

# ─── 3. NLTK resources ───────────────────────────
echo ""
echo " Downloading NLTK resources..."
python3 -c "
import nltk
for r in ['punkt','punkt_tab','stopwords','wordnet','averaged_perceptron_tagger','omw-1.4']:
    nltk.download(r, quiet=True)
print('   NLTK resources ready.')
"

# ─── 4. Train model if needed ────────────────────
if [ ! -f "model/fake_news_model.pkl" ]; then
  echo ""
  echo " Training ML model (first run)..."
  python3 model/train_model.py
else
  echo ""
  echo "✓  Trained model found."
fi

# ─── 5. Start Flask API ──────────────────────────
echo ""
echo " Starting Flask API on http://localhost:5000"
echo "   Open frontend/index.html in your browser."
echo ""
echo "   Press Ctrl+C to stop."
echo ""

export FLASK_ENV=development
python3 app.py
