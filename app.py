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
    id = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), nullable=False) 
    senha = db.Column(db.String(50), nullable=False) 

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    titulo = db.Column(db.String(100), nullable=False) 
    descricao = db.Column(db.Text, nullable=False)
    data_evento = db.Column(db.Date, nullable=False) 
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(email = email).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('eventos'))
        else: 
            flash('Login inválido. Verifique suas credenciais.')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = bcrypt.generate_password_hash(request.form.get('senha')).decode('utf-8')
        novo_usuario = Usuario(nome = nome, email = email, senha = senha)

        db.session.add(novo_usuario)
        db.session.commit()
        flash('Cadastro realizado com sucesso! Faça seu login.')
        return redirect(url_for('login'))

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
