import os
import simple_websocket

from pathlib import Path
from flask import Flask, render_template, url_for, redirect, session, request
from flask_socketio import SocketIO, send
from dotenv import load_dotenv
from models import db, Users

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

socketio = SocketIO(app, cors_allowed_origins='*')
app.config['SQLALCHEMY_TRACK_MODIFIVATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE')
db.init_app(app)
with app.app_context():
        db.create_all()


@socketio.on('message')
def handle_message(data):
    print(f'Message: {data}')
    send(data, broadcast=True)
    message = Users(username=data['username'], msg=data['msg'])
    try:
        db.session.add(message)
        db.session.commit()
    except:
        db.session.rollback()
        print('mistake')

@app.route('/')
def index():
    print(session)
    username = None
    if session.get('username'):
        username = session.get('username')
    return render_template('index.html', username=username)

@app.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        session['username'] = username
    return redirect(url_for('index'))

@app.route('/logout', methods=('POST', 'GET'))
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app)

