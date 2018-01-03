from flask import Flask, render_template, redirect, url_for, request
from flask_socketio import SocketIO, send, emit
import os
import cv2
import numpy as np

images = ['https://firebasestorage.googleapis.com/v0/b/morphle-633c0.appspot.com/o/0M1514457781733%2FX37p0Y9p0Z0p0F71.JPG?alt=media&token=df66a865-1d7f-43bf-b775-00eea6b49d7d', 'https://firebasestorage.googleapis.com/v0/b/morphle-633c0.appspot.com/o/0M1514457781733%2FX36p0Y9p0Z0p0F68.JPG?alt=media&token=a3d65f88-ba62-4b8e-bec7-71bd4196c5e0', 'https://firebasestorage.googleapis.com/v0/b/morphle-633c0.appspot.com/o/0M1514457781733%2FX35p0Y9p0Z0p0F70.JPG?alt=media&token=d9fd461c-be1a-4e47-b793-81c57c025ecb']

x = list(np.load('x.pkl'))
y = list(np.load('y.pkl'))
w = list(np.load('w.pkl'))
h = list(np.load('h.pkl'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('http://localhost:9010')
    return render_template('login.html', error=error)


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)

@socketio.on('connect')
def connect():
    emit('ready', 'ok')
        
@socketio.on('change')
def change():
    emit('next', {"image": images, "x": x, "y": y, "w": w, "h": h})
    
@app.route('/')
def index():
    return render_template('index.html')    
    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug = True, port = 9010, use_reloader = True)
