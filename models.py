from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(100), nullable=False, unique=True)
    correo = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    posts = db.relationship('Post', back_populates='autor', lazy=True)

    def __str__(self):
        return self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    titulo = db.Column(db.String(100), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    fecha_create = db.Column(db.DateTime, default=datetime.utcnow)

    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    autor = db.relationship('User', back_populates='posts', lazy=True)
    categoria = db.relationship('Category', back_populates='posts', lazy=True)


class Comentary(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    texto = db.Column(db.String(100), nullable=False)
    fecha_create = db.Column(db.DateTime, default=datetime.utcnow)

    autor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    autor = db.relationship('User', lazy=True)
    post = db.relationship('Post', lazy=True)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(50), nullable=False, unique=True)

    posts = db.relationship('Post', back_populates='categoria', lazy=True)
