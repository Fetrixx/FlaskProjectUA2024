import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'proyectoWebFlask2024')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True  # activa el modo de depuración en SQLAlchemy, para ver las consultas SQL generadas.

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_database.db'

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY', 'proyectoWebFlask2024Production')  # Cambiar por un valor seguro en producción
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///production_database.db')
