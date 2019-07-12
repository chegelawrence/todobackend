from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todobackend.config.config import Config
from flask_cors import CORS
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    ma.init_app(app)
    db.init_app(app)
    from todobackend.todos.todos import todos_blueprint
    app.register_blueprint(todos_blueprint)
    return app