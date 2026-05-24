import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from flask_cors import CORS
from config import Config
from routes.predict_routes import predict_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, origins=Config.CORS_ORIGINS)
    app.register_blueprint(predict_bp, url_prefix="/api")

    @app.route("/")
    def index():
        return {"message": "TruthGuard API is running", "version": "1.0"}

    return app


if __name__ == "__main__":
    app = create_app()
    print("\n" + "═" * 50)
    print("  TruthGuard API — Starting...")
    print("  http://localhost:5000")
    print("═" * 50 + "\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
