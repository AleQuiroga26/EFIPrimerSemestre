from flask import (  # importo todo lo que necesito para hacer la app web y manejar formularios, sesiones, mensajes, etc.
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
)
from flask_migrate import (
    Migrate,
)  # para manejar migraciones de la base de datos (cambios en tablas)
from flask_sqlalchemy import (
    SQLAlchemy,
)  # para trabajar con la base de datos usando objetos de Python
from werkzeug.security import (
    generate_password_hash,
)  # para guardar contraseñas encriptadas
import os
from dotenv import (
    load_dotenv,
)  # para cargar variables desde un archivo .env (configuración secreta)

load_dotenv()  # traigo esas variables (como la URL de la base de datos y la clave secreta)

app = Flask(__name__)  # creo la app

# configuro la conexión a la base de datos y la clave para las sesiones usando lo que cargué del .env
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.secret_key = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)  # inicio la base de datos
migrate = Migrate(app, db)  # inicio el sistema de migraciones para la base

from models import User, Post, Comentary, Category  # traigo mis tablas (modelos)


# Esto sirve para que la lista de categorías esté disponible en todas las plantillas, sin tener que pasarla en cada ruta
@app.context_processor
def injectar_categorias():
    categorias = Category.query.order_by(
        Category.id
    ).all()  # traigo las categorías ordenadas por id
    return dict(
        categorias=categorias
    )  # las pongo disponibles como variable 'categorias' en los templates


@app.route("/")  # ruta principal que muestra los posts
def index():
    posts_list = Post.query.order_by(
        Post.fecha_create.desc()
    ).all()  # traigo todos los posts ordenados por fecha, del más nuevo al más viejo
    return render_template(
        "index.html", posts=posts_list
    )  # mando esa lista a la plantilla para mostrarla


@app.route("/nuevo_post", methods=["GET", "POST"])  # ruta para crear un post nuevo
def nuevo_post():

    # si no está logueado, lo mando a la página de login
    if "user_id" not in session:
        flash("Debes iniciar sesión para crear un post.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        # saco los datos que el usuario puso en el formulario
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]
        categoria_id = request.form["categoria_id"]

        # creo el post nuevo y lo asocio con el usuario que está logueado
        nuevo = Post(
            titulo=titulo,
            contenido=contenido,
            categoria_id=categoria_id,
            autor_id=session["user_id"],
        )

        db.session.add(nuevo)  # lo agrego a la base de datos
        db.session.commit()  # guardo los cambios
        flash("Post creado con éxito.", "success")
        return redirect(url_for("index"))  # vuelvo al inicio

    return render_template(
        "nuevoPost.html"
    )  # si entró por GET, muestro el formulario para crear post


@app.route("/register", methods=["GET", "POST"])  # ruta para registrarse
def register():
    if request.method == "POST":
        # saco datos del formulario y elimino espacios al principio y final
        name = request.form["name"].strip()
        correo = request.form["correo"].strip()
        password = request.form["password"]
        password2 = request.form["password2"]

        # chequeo que no falte ningún dato
        if not name or not correo or not password:
            flash("Por favor, completá todos los campos.", "danger")
            return redirect(url_for("register"))

        # chequeo que no haya otro usuario con el mismo nombre o correo
        existe_nombre = User.query.filter_by(name=name).first()
        existe_correo = User.query.filter_by(correo=correo).first()
        if existe_nombre:
            flash("El nombre de usuario ya existe.", "danger")
            return redirect(url_for("register"))
        if existe_correo:
            flash("El correo ya está registrado.", "danger")
            return redirect(url_for("register"))

        # chequeo que las contraseñas coincidan
        if password != password2:
            flash("Las contrasenias no coinciden.", "danger")
            return redirect(url_for("register"))

        # guardo la contraseña encriptada para no guardar la original
        password_hash = generate_password_hash(password)

        # creo y guardo el nuevo usuario en la base
        nuevo_usuario = User(name=name, correo=correo, password=password_hash)
        db.session.add(nuevo_usuario)
        db.session.commit()

        flash("Usuario registrado con éxito.", "success")
        return redirect(url_for("index"))  # lo mando al inicio después de registrarse

    return render_template(
        "register.html"
    )  # si entró por GET, muestro el formulario para registrarse


from werkzeug.security import check_password_hash  # para verificar contraseñas


@app.route("/login", methods=["GET", "POST"])  # ruta para iniciar sesión
def login():
    if request.method == "POST":
        name = request.form["name"].strip()
        password = request.form["password"]

        # valido que no falten datos
        if not name or not password:
            flash("Por favor, completá todos los campos.", "danger")
            return redirect(url_for("login"))

        # busco al usuario por nombre
        usuario = User.query.filter_by(name=name).first()
        if not usuario:
            flash("Nombre de usuario o contraseña incorrectos.", "danger")
            return redirect(url_for("login"))

        # verifico que la contraseña sea correcta
        if not check_password_hash(usuario.password, password):
            flash("Nombre de usuario o contraseña incorrectos.", "danger")
            return redirect(url_for("login"))

        # si está todo bien, guardo el usuario en la sesión para que quede logueado
        session["user_id"] = usuario.id
        session["user_name"] = usuario.name

        flash("Has iniciado sesión correctamente.", "success")
        return redirect(url_for("index"))

    return render_template("login.html")  # formulario para login


@app.route("/logout")  # cerrar sesión
def logout():
    session.clear()  # borro todo de la sesión para desconectarlo
    flash("Has cerrado sesión.", "success")
    return redirect(url_for("index"))  # vuelvo al inicio


@app.route(
    "/post/<int:post_id>", methods=["GET", "POST"]
)  # página para ver un post y agregar comentarios
def ver_post(post_id):
    post = Post.query.get_or_404(
        post_id
    )  # busco el post o muestro error 404 si no existe

    if request.method == "POST":
        # para agregar un comentario nuevo

        # si no está logueado, lo mando a login
        if "user_id" not in session:
            flash("Debes iniciar sesión para comentar.")
            return redirect(url_for("login"))

        texto = request.form.get("texto", "").strip()
        # el comentario no puede estar vacío
        if not texto:
            flash("El comentario no puede estar vacío.")
            return redirect(url_for("ver_post", post_id=post_id))

        # creo el comentario y lo guardo relacionado al usuario y al post
        nuevo_comentario = Comentary(
            texto=texto, autor_id=session["user_id"], post_id=post_id
        )

        db.session.add(nuevo_comentario)
        db.session.commit()
        flash("Comentario agregado.")
        return redirect(url_for("ver_post", post_id=post_id))

    # traigo todos los comentarios del post ordenados de más antiguos a más nuevos
    comentarios = (
        Comentary.query.filter_by(post_id=post_id)
        .order_by(Comentary.fecha_create.asc())
        .all()
    )

    # envío a la plantilla el post y los comentarios para mostrarlos
    return render_template("verPost.html", post=post, comentarios=comentarios)


if __name__ == "__main__":
    app.run(
        debug=True
    )  # modo debug se reinicia sola cuando cambio algo
