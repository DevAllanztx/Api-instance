from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'FSD2323F#$!SAH'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blug.db'

db = SQLAlchemy(app)
db: SQLAlchemy


class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer, db.ForeignKey('autor.id_autor'))

class Autor(db.Model):
    __tablename__ = 'autor' 
    id_autor = db.Column(db.Integer, primary_key=True) 
    nome = db.Column(db.String)  # Adicionando o campo nome
    email = db.Column(db.String)
    senha = db.Column(db.String)
    admin = db.Column(db.Boolean)
    postagens = db.relationship('Postagem') 


with app.app_context():
    db.drop_all()
    db.create_all()
    autor = Autor(nome='Allan', email='allanaugusto2077@gmail.com', 
                  senha='123456', admin=True)
    db.session.add(autor)
    db.session.commit()

