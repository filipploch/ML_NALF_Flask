# main.py

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    ma.init_app(app)

    from app.views.controller.controller_views import controller_blueprint
    app.register_blueprint(controller_blueprint)

    create_database(app)
    return app


def create_database(app):
    with app.app_context():
        if not path.exists('instance/database.db'):
            db.create_all()
            print('db created')
