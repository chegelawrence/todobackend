from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from todobackend.config.config import Config
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
blacklist = set()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    #allow Cross Origin Resource Sharing on every route
    CORS(app)
    ma.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    Migrate(app,db)
    from todobackend.todos.todos import todos_blueprint
    from todobackend.users.users import users_blueprint
    app.register_blueprint(todos_blueprint)
    app.register_blueprint(users_blueprint)
    return app