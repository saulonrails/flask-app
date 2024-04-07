from flask import Flask, render_template, request, redirect, session, flash, url_for

class Album:
    def __init__(self, nome, artista, genero):
        self.nome = nome
        self.artista = artista
        self.genero = genero

album1 = Album('Boys For Pele', 'Tori Amos', 'Pop barroco')
album2 = Album('To Bring You My Love', 'PJ Harvey', 'Rock alternativo')
album3 = Album('When The Pawn...', 'Fiona Apple', 'Jazz')
lista = [album1, album2, album3]

class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = Usuario("Marianne Becker", "Marie", "ridofme")
usuario2 = Usuario("Ian Ferreira", "SonicIan", "fortheroses")
usuario3 = Usuario("Patrick Brainbridge", "Hooshik", "loveridden")

usuarios = { usuario1.nickname : usuario1,
             usuario2.nickname : usuario2,
             usuario3.nickname : usuario3 }

app = Flask(__name__)
app.secret_key = 'noiselessnoise'

@app.route('/')
def index():
    return render_template('lista.html', titulo='Álbuns', albuns=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Álbum')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    artista = request.form['artista']
    genero = request.form['genero']
    album = Album(nome, artista, genero)
    lista.append(album)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST',])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Você foi desconectado.')
    return redirect(url_for('index'))

app.run(debug=True)