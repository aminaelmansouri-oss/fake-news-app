from flask import Blueprint, request, jsonify
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from services.prediction_service import predict
from scraper.scraper import scrape_article
from database.db import save_analysis, get_history, get_stats

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict/text", methods=["POST"])
def predict_text():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    text = data["text"].strip()
    if len(text) < 20:
        return jsonify({"error": "Text too short. Please provide at least 20 characters."}), 400

    result = predict(text)
    if "error" in result:
        return jsonify(result), 422

    # Save to history
    result["input_type"] = "text"
    result["source"] = "Manual input"
    save_analysis(result)

    return jsonify(result)


@predict_bp.route("/predict/url", methods=["POST"])
def predict_url():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    url = data["url"].strip()
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "Invalid URL. Must start with http:// or https://"}), 400

    # Scrape
    scrape_result = scrape_article(url)
    if not scrape_result["success"]:
        return jsonify({"error": scrape_result["error"]}), 422

    # Predict
    result = predict(scrape_result["text"])
    if "error" in result:
        return jsonify(result), 422

    result["input_type"] = "url"
    result["source"] = url
    result["scraped_title"] = scrape_result.get("title", "")
    save_analysis(result)

    return jsonify(result)


@predict_bp.route("/history", methods=["GET"])
def history():
    limit = request.args.get("limit", 50, type=int)
    rows = get_history(limit)
    return jsonify(rows)


@predict_bp.route("/stats", methods=["GET"])
def stats():
    data = get_stats()
    return jsonify(data)


@predict_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "TruthGuard API"})
