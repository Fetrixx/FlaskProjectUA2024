from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
import pytz

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(pytz.utc))  # Almacena en UTC
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note', backref='author', lazy=True)
    
    # Nuevas relaciones para seguimiento
    followed = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed_user', lazy='dynamic')

class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='publications')  # Relación con el usuario
    

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)  # Para comentarios anidados
    
    user = db.relationship('User', backref='comments')
    publication = db.relationship('Publication', backref='comments')
    parent = db.relationship('Comment', remote_side=[id], backref='replies')  # Relación recursiva