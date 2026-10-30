import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "hydroflow-secure-dev-session-key-2026")
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "instance" / "hydroflow.db"))
    
    # Server configuration
    PORT = int(os.getenv("PORT", 3000))
    HOST = os.getenv("HOST", "0.0.0.0")
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("true", "1", "t")
    
    # IoT Device Configuration
    DEVICE_ID = os.getenv("DEVICE_ID", "ESP32-001")
    DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() in ("true", "1", "t")
    SENSOR_STALE_SECONDS = int(os.getenv("SENSOR_STALE_SECONDS", 30))
    
    # EMQX MQTT Configuration
    EMQX_HOST = os.getenv("EMQX_HOST", "")
    EMQX_PORT = int(os.getenv("EMQX_PORT", 8883))
    EMQX_USERNAME = os.getenv("EMQX_USERNAME", "")
    EMQX_PASSWORD = os.getenv("EMQX_PASSWORD", "")
    EMQX_CLIENT_ID = os.getenv("EMQX_CLIENT_ID", "hydroflow-backend")
    EMQX_USE_TLS = os.getenv("EMQX_USE_TLS", "true").lower() in ("true", "1", "t")
    EMQX_CA_CERT_PATH = os.getenv("EMQX_CA_CERT_PATH", "")
    EMQX_KEEPALIVE = int(os.getenv("EMQX_KEEPALIVE", 60))
    
    # ThingSpeak Cloud Configuration
    THINGSPEAK_API_KEY = os.getenv("THINGSPEAK_API_KEY", "")
    THINGSPEAK_CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID", "")
    THINGSPEAK_READ_API_KEY = os.getenv("THINGSPEAK_READ_API_KEY", "")
    
    # Upload folder
    UPLOAD_FOLDER = str(BASE_DIR / "static" / "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
