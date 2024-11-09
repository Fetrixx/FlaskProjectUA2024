from .. import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    username = db.Column(db.String(150), unique=True)
    profile_picture = db.Column(db.String(200), default='https://t3.ftcdn.net/jpg/06/33/54/78/360_F_633547842_AugYzexTpMJ9z1YcpTKUBoqBF0CUCk10.jpg')  # URL de la imagen de perfil por defecto
    date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    
    # notes = db.relationship('Note', backref='author', lazy=True)
    # bio = db.Column(db.Text)  # Campo para la biografía
    
    
    # Nuevas relaciones para seguimiento
    followed = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed_user', lazy='dynamic')
    profile = db.relationship('Profile', backref='user', uselist=False)  # Relación uno a uno

    