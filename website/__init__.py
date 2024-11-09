import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Importar Flask-Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()  # Crear una instancia de Migrate



def create_app(config_class='config.Config'):  # Define la configuración por defecto como 'config.Config'
    app = Flask(__name__)
    app.config.from_object(config_class)  # Carga la configuración desde config.py
    
    db.init_app(app)
    migrate.init_app(app, db)  # Inicializar Flask-Migrate con la app y db


    from .views import register_blueprints
    register_blueprints(app)

    # Crear la base de datos si no existe
    if not os.path.exists(f"website/{app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1]}"):
        with app.app_context():
            db.create_all()
        print('Base de datos creada!')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models.user import User
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

