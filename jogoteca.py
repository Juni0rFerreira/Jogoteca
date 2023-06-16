from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome=nome
        self.categoria=categoria
        self.console=console

jogo1= Jogo('Tetris', 'Puzzle', 'Atari')
jogo2= Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3= Jogo('Mortal Kombat', 'Luta', 'PS2')
lista = [jogo1, jogo2, jogo3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome=nome
        self.nickname=nickname
        self.senha=senha

usuario1=Usuario("Junior", "Chaperoso", "12345")
usuario2=Usuario("Mariana", "Chaperosa", "12345")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2 }

app = Flask(__name__)
app.secret_key = 'Chaperoso'

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = '123456',
        servidor = 'localhost',
        database = 'jogoteca'
    )

db = SQLAlchemy(app)

class Jogos(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(50), nubllable=False)
    categoria = db.Column(db.String(40), nubllable=False)
    console = db.Column(db.String(20), nubllable=False)
    def __repr__(self):
        return '<Name %r>' % self.name
class Usuarios(db.Model):
    nickname = db.Column(db.String(8), primary_key=True)
    nome = db.Column(db.String(20), nubllable=False)
    senha = db.Column(db.String(100), nubllable=False)
    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/lista')
def index():
    return render_template('lista.html', titulo='JOGOS', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('/', proxima=url_for('novo')))
    return render_template('novo.html', titulo='ADICIONE UM NOVO JOGO')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/')
def login():
    proxima = request.args.get('proxima')
    return render_template('/login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            return redirect ('lista')
    else:
        flash('Usuário ou Senha incorreta!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))

app.run(debug=True)