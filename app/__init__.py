from flask import Flask
from flask_socketio import SocketIO

flask_app = Flask(__name__)
flask_app.secret_key = 'JHUHKG6876yuFH%Y$%^$5643%^'
all_users={}
socketio = SocketIO(flask_app) 

ENV = 'prod' #'dev'

from app import routes,gimage,all_users