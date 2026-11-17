from flask import Flask
from .config import Config
from .database import init_db
from .routes import web

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    init_db(app)
    app.register_blueprint(web)
    return app
