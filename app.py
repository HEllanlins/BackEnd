from flask import Flask, request, render_template, redirect, url_for, flash
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
login_manager.login_view = 'login'

class Usuario(db.Model, UserMixin):
    id = db.column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.Sftring(100), nullable=False) 
    senha = db.Column(db.Sftring(50), nullable=False) 

class Evento(db.Model):
    id = db.column(db.Integer, primary_key=True) 
    titulo = db.column(db.String(100), nullabel=False) 
    descricao = db.column(db.Text, nullabel=False)
    data_evento = db.column(db.Date, nullabel=False) 
    usuario_id = db.column(db.Integer, db.ForeignKey('usuario.id'), nullabel=False)
    

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
        novo_usuario = Usuario(nome = nome, email = email, senha = senha)
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
