#IMPORTAÇÕES
import os
from flask import flash
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from models import Usuario, Livro
from db import db
import hashlib

#INICIO JULIANA---------------------------------
project_dir = os.path.dirname(os.path.abspath(__file__))

database_file = "sqlite:///{}".format(os.path.join(project_dir,
"bookdatabase.db")) 

#INICIALIZAÇÃO
app = Flask(__name__)
app.secret_key = 'projetoPP2'#?
#QUANDO ELE NÃO TIVER AUTORIZAÇÃO, RETORNA PARA O LOGIN
lm = LoginManager(app)
lm.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
db.init_app(app)

#SENHA CRIPTOGRAFADA(SEGURA)
def hash(txt):
    hash_obj = hashlib.sha256(txt.encode('utf-8'))
    return hash_obj.hexdigest()

#FUNÇÃO P/LOGAR (TRABALHA COM ID)
@lm.user_loader
def user_loader(id):
    usuario = db.session.query(Usuario).filter_by(id=id).first()
    return usuario



#ROTAS
@app.route('/')
@login_required
def home():
    return render_template('site.html')

#login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method =='POST':
        nome=request.form['nomeForm']
        senha=request.form['senhaForm']

        user = db.session.query(Usuario).filter_by(nome=nome, senha=hash(senha)).first()
        if not user:
            return 'Nome ou senha incorretos. '
        
        login_user(user)
        return redirect(url_for('home'))


''
#Rota para navegar pelo menu (assim deu certo)
@app.route('/sobrenos')
def sobrenos():
        return render_template('sobrenos.html')
#Rota para navegar pelo menu (assim deu certo)
@app.route('/adicionar')
def adicionar():
        return render_template('adicionar_livro.html')
#Rota para navegar pelo menu (assim deu certo)
@app.route('/carrinho')
def carrinho():
        return render_template('carrinho.html')



#cadastro
@app.route('/cadastro', methods=['GET','POST'])
def registrar():
    if request.method == "GET":
        return render_template('cadastro.html')
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        email = request.form['emailForm']
        senha = request.form['senhaForm']

        #DICIONAR REGISTRO AO BANCO DE DADOS
        novo_usuario = Usuario(nome=nome, email=email, senha=hash(senha))
        db.session.add(novo_usuario)
        db.session.commit()

        #Login_usuario
        login_user(novo_usuario)

        #RETORNO
        return redirect(url_for('home'))
    

    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))




@app.route('/adicionar_livro', methods=['GET', 'POST'])
@login_required
def adicionar_livro():
   
    livros = Livro.query.all()
    print("Livros cadastrados:", livros)  
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        if titulo:
            novo_livro = Livro(titulo=titulo)
            db.session.add(novo_livro)
            db.session.commit()

            return redirect(url_for('adicionar_livro'))  
    return render_template('adicionar_livro.html', livros=livros)



@app.route('/remover_livro/<int:livro_id>', methods=['POST'])
@login_required
def remover_livro(livro_id):
    livro = Livro.query.get(livro_id)
    if livro:
        db.session.delete(livro)
        db.session.commit()
        flash('Livro removido com sucesso!', 'success')
    return redirect(url_for('adicionar_livro'))


@app.route('/buscar_livro', methods=['GET'])
@login_required
def buscar_livro():
    titulo = request.args.get('titulo')
    if titulo:

        livros = Livro.query.filter(Livro.titulo.ilike(f'%{titulo}%')).all()
    else:
        livros = Livro.query.all()
    
    return render_template('buscar_livro.html', livros=livros, titulo=titulo)


#ATIVAÇÃO DO BANCO DE DADOS
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


#PARTE DE JULIANA, FIM -------------------   