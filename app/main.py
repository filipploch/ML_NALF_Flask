# main.py

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_apscheduler import APScheduler
from app.obswebsocketpy import OBSWebsocket

db = SQLAlchemy()
ma = Marshmallow()
apscheduler = APScheduler()
obs_ws = OBSWebsocket()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    ma.init_app(app)
    apscheduler.init_app(app)
    obs_ws.init_app(app)
    app.config.update({'OBS_WS': obs_ws})
    # print(app.config.from_object('config.DevelopmentConfig'))
    # ['OBS_WS']. = obs_ws
    apscheduler.add_job(func=obs_ws.connect_websocket, args=[app], id='obswebsocketpy')
    apscheduler.start()

    from app.views.controller.controller_views import controller_blueprint
    app.register_blueprint(controller_blueprint)
    from app.views.obs_screen.obs_screen_views import obs_screen_blueprint
    app.register_blueprint(obs_screen_blueprint)

    create_database(app)
    return app


def create_database(app):
    with app.app_context():
        if not path.exists('instance/database.db'):
            db.create_all()
            print('db created')
