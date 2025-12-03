# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, "flynn.db")
LOG_PATH = os.path.join(LOG_DIR, "system.log")

LOCKOUT_THRESHOLD = 5       # 5 yanlış şifre
LOCKOUT_TIME = 300          # saniye (5 dakika)
