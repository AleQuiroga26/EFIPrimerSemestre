from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Conexion a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/dbEFI_PS"
db = SQLAlchemy(app)

migrate = Migrate(app, db)  #modulo que nos ayuda a cargar nuestras entidades

from models import User

@app.route('/')
def index():
    return render_template(
        "index.html"
    )