from flask import Flask,jsonify
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
    return app