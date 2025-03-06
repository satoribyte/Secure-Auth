import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(DATA_DIR, 'data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = os.path.join(BASE_DIR, 'logs', 'app.log')
    ERROR_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'error.log')
    ACCESS_LOG_FILE = os.path.join(BASE_DIR, 'logs', 'access.log')
    JSON_FILE = os.path.join(DATA_DIR, 'users.json')