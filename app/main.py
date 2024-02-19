# main.py

from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_apscheduler import APScheduler
from app.obswebsocketpy import OBSWebsocket
from flask_socketio import SocketIO

db = SQLAlchemy()
ma = Marshmallow()
apscheduler = APScheduler()
obs_ws = OBSWebsocket()
socketio = SocketIO()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    db.init_app(app)
    app.config.update({'DB': db})
    ma.init_app(app)
    apscheduler.init_app(app)
    app.config.update({'APSHEDULER': apscheduler})
    socketio.init_app(app)
    app.config.update({'SOCKETIO': socketio})
    obs_ws.init_app(app)
    app.config.update({'OBS_WS': obs_ws})
    # obs_ws.register(obs_ws.on_event)
    # obs_ws.register(obs_ws.on_switch, events.SwitchScenes)
    # obs_ws.register(obs_ws.on_switch, events.CurrentProgramSceneChanged)
    obs_ws.connect_websocket(app)
    # apscheduler.add_job(func=obs_ws.connect_websocket, args=[app], id='obswebsocketpy')
    # apscheduler.start()

    from app.views.controller.controller_views import controller_blueprint
    app.register_blueprint(controller_blueprint)
    from app.views.obs_screen.obs_screen_views import obs_screen_blueprint
    app.register_blueprint(obs_screen_blueprint)

    # if app.debug:
    #     import logging
    #     logging.basicConfig(level=logging.DEBUG)

    create_database(app)
    return app


def create_database(app):
    with app.app_context():
        if not path.exists('instance/database.db'):
            db.create_all()
            print('db created')
