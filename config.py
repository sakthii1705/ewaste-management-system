import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _db_uri(db_name):
    user = os.getenv("DB_USER", "root")
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "3306")
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}?charset=utf8mb4"


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = _db_uri(os.getenv("DB_NAME", "ewaste_db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True, "pool_recycle": 280}

    # Security
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False  # True in production (HTTPS)
    REMEMBER_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 2  # 2 hours

    # App settings
    LOW_STOCK_THRESHOLD = int(os.getenv("LOW_STOCK_THRESHOLD", 5))
    ITEMS_PER_PAGE = int(os.getenv("ITEMS_PER_PAGE", 10))
    QR_FOLDER = os.path.join(os.path.dirname(__file__), "app", "static", "qr")
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2 MB


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = _db_uri(os.getenv("TEST_DB_NAME", "ewaste_test_db"))
    WTF_CSRF_ENABLED = False  # tests post forms directly
    SECRET_KEY = "testing-secret-key"


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config():
    name = os.getenv("FLASK_ENV", "development")
    cfg = config_by_name.get(name, DevelopmentConfig)
    if not cfg.SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set. Copy .env.example to .env and set it.")
    return cfg