from app import flask_app,socketio
from flask import Flask
'''
host = '127.0.0.1'
port = 5000
'''
DEBUG = 0
if __name__ == "__main__":
    #Flask.run(flask_app,host=host,port=port,debug = DEBUG)
    socketio.run(app=flask_app,host='127.0.0.1',port=6000)