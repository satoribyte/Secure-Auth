import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=None):
    if config_class is None:
        config_class = os.getenv('FLASK_CONFIG', 'config.Config')

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.user import User  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    logs_dir = 'logs'
    os.makedirs(logs_dir, exist_ok=True)
    log_level = logging.DEBUG if app.config.get("ENV") == "development" else logging.INFO

    log_files = {
        'log': app.config.get('LOG_FILE', os.path.join(logs_dir, 'app.log')),
        'error': app.config.get('ERROR_LOG_FILE', os.path.join(logs_dir, 'error.log')),
        'access': app.config.get('ACCESS_LOG_FILE', os.path.join(logs_dir, 'access.log')),
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    for log_type, log_file in log_files.items():
        handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=3)
        handler.setFormatter(formatter)
        handler.setLevel(logging.ERROR if log_type == 'error' else log_level)
        app.logger.addHandler(handler)

    if app.config.get("ENV") == "development":
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(console_handler)

    app.logger.setLevel(log_level)
    app.logger.info("Flask app started, logging is active.")

    from app.routes.auth import auth
    from app.routes.dashboard import dashboard
    from app.routes.home import home
    from app.routes.error import errors
    
    app.register_blueprint(auth)
    app.register_blueprint(dashboard)
    app.register_blueprint(home)
    app.register_blueprint(errors)
    
    return app