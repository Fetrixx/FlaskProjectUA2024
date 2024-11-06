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
    username = db.Column(db.String(150), unique=True)
    profile_picture = db.Column(db.String(200), default='https://t3.ftcdn.net/jpg/06/33/54/78/360_F_633547842_AugYzexTpMJ9z1YcpTKUBoqBF0CUCk10.jpg')  # URL de la imagen de perfil por defecto
    date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # notes = db.relationship('Note', backref='author', lazy=True)
    # bio = db.Column(db.Text)  # Campo para la biografía
    
    
    # Nuevas relaciones para seguimiento
    followed = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower', lazy='dynamic')
    followers = db.relationship('Follow', foreign_keys='Follow.followed_id', backref='followed_user', lazy='dynamic')
    profile = db.relationship('Profile', backref='user', uselist=False)  # Relación uno a uno

    
    
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)  # Relación uno a uno
    bio = db.Column(db.Text)  # Biografía
    background_picture = db.Column(db.String(200), default='https://media.istockphoto.com/id/1223483739/vector/seamless-pattern-with-user-experience-icons.jpg?s=612x612&w=0&k=20&c=AYDPQuJQVAKoVjl8qYDP4C53ZvmZXGIwPhJpquB6gus=')  # URL de la imagen de perfil por defecto

    # user = db.relationship('User', backref='profile')  # Relación inversa


class Follow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    data = db.Column(db.String(10000))
    content_type = db.Column(db.String(50))  # Ejemplo: 'text', 'image', 'video'
    image_url = db.Column(db.String(200), nullable=True)  # URL de la imagen
    video_url = db.Column(db.String(200), nullable=True)  # URL del video
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='publications')  # Relación con el usuario
    likes_count = db.Column(db.Integer, default=0)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)  # Para comentarios anidados
    likes_count = db.Column(db.Integer, default=0)
    
    user = db.relationship('User', backref='comments')
    publication = db.relationship('Publication', backref='comments')
    parent = db.relationship('Comment', remote_side=[id], backref='replies')  # Relación recursiva
    
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publication_id = db.Column(db.Integer, db.ForeignKey('publication.id'), nullable=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref='likes')
    publication = db.relationship('Publication', backref='likes', foreign_keys=[publication_id])
    comment = db.relationship('Comment', backref='likes', foreign_keys=[comment_id])

    # Método para asegurar que el like esté en una publicación o un comentario, pero no ambos.
    def __init__(self, user_id, publication_id=None, comment_id=None):
        if publication_id and comment_id:
            raise ValueError("A like cannot be associated with both a publication and a comment at the same time.")
        if not publication_id and not comment_id:
            raise ValueError("A like must be associated with either a publication or a comment.")
        self.user_id = user_id
        self.publication_id = publication_id
        self.comment_id = comment_id

    
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())

    user = db.relationship('User', backref='notifications')