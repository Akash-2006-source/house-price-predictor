import os
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = 'sqlite:////data/history.db' if Path('/data').is_dir() and os.access('/data', os.W_OK) else f"sqlite:///{ROOT / 'history.db'}"
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'development-only-change-me')
    DATABASE_URL = os.getenv('DATABASE_URL', DEFAULT_DB)
    MAX_HISTORY_RECORDS = int(os.getenv('MAX_HISTORY_RECORDS', '50'))
    ARTIFACT_PATH = ROOT / 'artifacts' / 'model.joblib'
    METRICS_PATH = ROOT / 'artifacts' / 'metrics.json'
