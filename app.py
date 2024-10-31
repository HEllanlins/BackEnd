from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from datetime import datetime


app = Flask(__name__)

app.config['SECRET_KEY'] = 'seu_segredo'

#caminho para o banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'ecoceub.db')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

class Usuario(db.Model, UserMixin):
    id = db.column(db.integer, primary_key=true)
    nome = db.Column(db.sftring(100), nullable=false)
    email = db.Column(db.sftring(100), nullable=false)
    senha = db.Column(db.sftring(50), nullable=false)
    

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register', methods=['Get', 'Post'])
def register():
    if request.method == 'Post':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
