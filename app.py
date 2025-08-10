from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
) # importamos Flask y las funciones necesarias para manejar las plantillas y las solicitudes

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

#Conexion a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/dbEFI_PS"
db = SQLAlchemy(app)

migrate = Migrate(app, db)  #modulo que nos ayuda a cargar nuestras entidades

from models import User, Post, Comentary, Category

@app.route('/')
def index():
    posts_list = Post.query.order_by(Post.fecha_create.desc()).all()
    return render_template("index.html", posts=posts_list) #nombre_en_html = nombre_en_back

@app.route('/nuevo_post', methods=['GET', 'POST'])
def nuevo_post():
    if request.method == "POST":
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]
        categoria_id = request.form["categoria_id"]

        nuevo = Post(titulo=titulo, contenido=contenido, categoria_id=categoria_id)
        db.session.add(nuevo)
        db.session.commit()
        return redirect(url_for("index"))
    
    categorias = Category.query.all()
    return render_template("nuevo_post.html", categorias=categorias)

