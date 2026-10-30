import os
import sys
import argparse
from pathlib import Path
from flask import Flask, render_template, send_from_directory, jsonify

# Add root directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from config import Config
from database.seed import seed_database
from services.mqtt_service import mqtt_service

# Import Blueprints
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.sensors import sensors_bp
from routes.esp32 import esp32_bp
from routes.actuators import actuators_bp
from routes.automation import automation_bp
from routes.analytics import analytics_bp
from routes.plant_health import plant_health_bp
from routes.alerts import alerts_bp
from routes.device import device_bp
from routes.connectivity import connectivity_bp
from routes.logs import logs_bp

def create_app():
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
        static_url_path="/static"
    )

    app.config.from_object(Config)

    # Initialize and seed database if not already done
    try:
        seed_database()
    except Exception as e:
        print(f"Database initialization notice: {e}")

    # Register API Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(sensors_bp, url_prefix="/api")
    app.register_blueprint(esp32_bp, url_prefix="/api")
    app.register_blueprint(actuators_bp, url_prefix="/api")
    app.register_blueprint(automation_bp, url_prefix="/api")
    app.register_blueprint(analytics_bp, url_prefix="/api")
    app.register_blueprint(plant_health_bp, url_prefix="/api")
    app.register_blueprint(alerts_bp, url_prefix="/api")
    app.register_blueprint(device_bp, url_prefix="/api")
    app.register_blueprint(connectivity_bp, url_prefix="/api")
    app.register_blueprint(logs_bp, url_prefix="/api")

    # Start MQTT background service if host configured
    try:
        mqtt_service.start()
    except Exception as e:
        print(f"MQTT Service notice: {e}")

    # Frontend Page Routes (All render master index.html)
    @app.route("/")
    @app.route("/login")
    @app.route("/dashboard")
    @app.route("/live-monitoring")
    @app.route("/analytics")
    @app.route("/plant-health")
    @app.route("/alerts")
    @app.route("/automation")
    @app.route("/device")
    @app.route("/logs")
    def index():
        return render_template("index.html")

    # Health check endpoint
    @app.route("/api/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "HYDROFLOW",
            "demo_mode": Config.DEMO_MODE,
            "device_id": Config.DEVICE_ID
        })

    # Serve static assets fallback
    @app.route("/assets/<path:path>")
    def send_assets(path):
        return send_from_directory(str(BASE_DIR / "static"), path)

    return app

app = create_app()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HYDROFLOW Smart IoT Hydroponics Backend")
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", 3000)), help="Port to run server on")
    parser.add_argument("--host", type=str, default=os.getenv("HOST", "0.0.0.0"), help="Host IP to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")
    args = parser.parse_args()

    print(f"\n============================================================")
    print(f" HYDROFLOW - Smart IoT Hydroponics Management System")
    print(f" Server running at: http://{args.host}:{args.port}")
    print(f" Device ID: {Config.DEVICE_ID}")
    print(f" Demo Mode: {Config.DEMO_MODE}")
    print(f" Database: {Config.DATABASE_PATH}")
    print(f"============================================================\n")

    app.run(host=args.host, port=args.port, debug=args.debug)
