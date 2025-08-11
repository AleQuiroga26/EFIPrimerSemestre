from app import db
from datetime import datetime  # para manejar fechas y horas


# Modelo que representa a los usuarios
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id único para cada usuario
    name = db.Column(
        db.String(100), nullable=False, unique=True
    )  # nombre de usuario, no puede repetirse ni estar vacío
    correo = db.Column(
        db.String(100), nullable=False, unique=True
    )  # mail único y obligatorio
    password = db.Column(
        db.String(255), nullable=False
    )  # contraseña guardada encriptada

    posts = db.relationship("Post", back_populates="autor", lazy=True)
    # relación para poder acceder a todos los posts que hizo este usuario

    def __str__(self):
        return self.name  # para que cuando imprimo el usuario salga su nombre


# Modelo para los posts o entradas del blog
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id único para cada post
    titulo = db.Column(db.String(100), nullable=False)  # título del post, obligatorio
    contenido = db.Column(db.Text, nullable=False)  # contenido del post, obligatorio
    fecha_create = db.Column(db.DateTime, default=datetime.utcnow)
    # fecha y hora de creación, se pone automáticamente al crearlo

    autor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # vínculo con el usuario que hizo el post (no puede estar vacío)
    categoria_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=True)
    # vínculo con la categoría, puede no tener categoría

    autor = db.relationship("User", back_populates="posts", lazy=True)
    # relación para acceder fácilmente al usuario que creó el post
    categoria = db.relationship("Category", back_populates="posts", lazy=True)
    # relación para acceder a la categoría a la que pertenece el post


# Modelo para los comentarios que hacen los usuarios en los posts
class Comentary(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id único para cada comentario
    texto = db.Column(
        db.String(100), nullable=False
    )  # texto del comentario, obligatorio
    fecha_create = db.Column(db.DateTime, default=datetime.utcnow)
    # fecha y hora en que se hizo el comentario

    autor_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    # vínculo con el usuario que escribió el comentario
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    # vínculo con el post al que pertenece el comentario

    autor = db.relationship("User", lazy=True)  # para acceder al autor del comentario
    post = db.relationship("Post", lazy=True)  # para acceder al post correspondiente


# Modelo para las categorías de los posts
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id único para cada categoría
    name = db.Column(
        db.String(50), nullable=False, unique=True
    )  # nombre único y obligatorio de la categoría

    posts = db.relationship("Post", back_populates="categoria", lazy=True)
    # relación para acceder a todos los posts que están en esta categoría
