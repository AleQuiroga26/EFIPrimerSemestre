from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False, unique=True)
    correo = db.Column(db.String(100),nullable=False, unique=True)
    password = db.Column(db.String(100),nullable=False)

    def __str__(self):
        return self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_create = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

class Comentary(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    texto = db.Column(db.String(100), nullable=False)
    fecha_create = db.Column(db.DateTime, default=datetime.utcnow)
    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False, unique=True)

