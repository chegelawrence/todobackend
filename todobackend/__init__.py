from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from todobackend.config.config import Config
import os

DB_URI = os.path.join(os.path.dirname(__file__),'todos.sqlite')

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app