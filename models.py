from db import db
#PARA SER IDENTIFICADO COMO CLASSE DE USUARIO
from flask_login import UserMixin

class Usuario(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(30), unique=True)
    email= db.Column(db.String(30), unique=True)
    senha = db.Column(db.String())

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    def __init__(self, titulo):
        self.titulo = titulo