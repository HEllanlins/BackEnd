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

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecoceub.db'

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

#criação das tabelas no banco de dados
with app.app_context():
    db.create_all()

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

@app.route('/eventos', methods=['GET', 'POST'])
@login_required
def eventos():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        data_evento = request.form.get('data_evento')

        #converter a string para um objeto datetime
        data_evento_convertida = datetime.strptime(data_evento, '%Y-%m-%d').date()

        novo_evento = Evento(titulo = titulo, descricao = descricao, data_evento = data_evento_convertida, usuario_id = current_user.id)

        db.session.add(novo_evento)
        db.session.commit()
        flash('Evento cadastrado com sucesso!')

    #pegar a data atual
    data_atual = datetime.now().strftime('%Y-%m-%d')

    eventos = Evento.query.filter(Evento.data_evento >= datetime.now().date()).order_by(Evento.data_evento.asc()).all()

    return render_template('eventos.html', eventos=eventos)

@app.route('/agenda')
def agendas():
    # Obter a data atual para filtrar os eventos
    data_atual = datetime.now().strftime('%Y-%m-%d')

    # Pegar o número da página atual na query string da URL, ou usar 1 como padrão
    page = request.args.get('page', 1, type=int)

    # Filtrar eventos futuros e ordenar pela data mais próxima, usando paginação
    eventos_paginados = Evento.query.filter(Evento.data_evento >= data_atual)\
        .order_by(Evento.data_evento.asc())\
        .paginate(page=page, per_page=10)

    return render_template('agenda.html', eventos=eventos_paginados)

if __name__ == '__main__':
    app.run(debug=True)
