import eventlet
from flask import Flask
from flask_socketio import SocketIO

flask_app = Flask(__name__)

socketio = SocketIO(flask_app) 

from app import routes,gimage