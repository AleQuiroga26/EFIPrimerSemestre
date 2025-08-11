from app import app, db  # traigo la app y la base de datos para poder usarla
from models import Category  # traigo la tabla de categorías

# Lista con las categorías que quiero tener ya creadas en la base
categorias_predefinidas = [
    "Tecnología",
    "Deportes",
    "Cultura",
    "Noticias",
    "Entretenimiento",
    "Otro",
]

# Esto es para que pueda usar la base de datos fuera de una ruta (contexto de app)
with app.app_context():
    # Recorro cada nombre en la lista de categorías
    for nombre in categorias_predefinidas:
        # Si no existe esa categoría en la base, la creo y la agrego
        if not Category.query.filter_by(name=nombre).first():
            db.session.add(Category(name=nombre))
    # Guardo todos los cambios de una vez
    db.session.commit()

    print("Categorías insertadas correctamente.")  # aviso que terminó bien
