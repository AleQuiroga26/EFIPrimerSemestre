from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()  # carga las variables del archivo .env

app = Flask(__name__)

# Configuraciones usando variables de entorno
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.secret_key = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    return render_template("nuevoPost.html", categorias=categorias)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        correo = request.form['correo'].strip()
        password = request.form['password']
        password2 = request.form['password2']

        # Validar campos vacíos
        if not name or not correo or not password:
            flash('Por favor, completá todos los campos.', 'danger')
            return redirect(url_for('register'))

        # Validar que no exista otro usuario con mismo nombre o correo
        existe_nombre = User.query.filter_by(name=name).first()
        existe_correo = User.query.filter_by(correo=correo).first()
        if existe_nombre:
            flash('El nombre de usuario ya existe.', 'danger')
            return redirect(url_for('register'))
        if existe_correo:
            flash('El correo ya está registrado.', 'danger')
            return redirect(url_for('register'))
        
        if password != password2:
            flash('Las contrasenias no coinciden.', 'danger')
            return redirect(url_for('register'))

        # Hashear contraseña 
        password_hash = generate_password_hash(password)

        # Crear nuevo usuario
        nuevo_usuario = User(name=name, correo=correo, password=password_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario registrado con éxito.', 'success')
        return redirect(url_for('index')) 

    return render_template('register.html')

from werkzeug.security import check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name'].strip()
        password = request.form['password']

        # Validar campos vacíos
        if not name or not password:
            flash('Por favor, completá todos los campos.', 'danger')
            return redirect(url_for('login'))

        # Buscar usuario por nombre
        usuario = User.query.filter_by(name=name).first()
        if not usuario:
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))

        # Verificar contraseña
        if not check_password_hash(usuario.password, password):
            flash('Nombre de usuario o contraseña incorrectos.', 'danger')
            return redirect(url_for('login'))
        
        session['user_id'] = usuario.id
        session['user_name'] = usuario.name

        flash('Has iniciado sesión correctamente.', 'success')
        return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()  
    flash('Has cerrado sesión.', 'success')
    return redirect(url_for('index'))
