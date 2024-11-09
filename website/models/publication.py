from .. import db
from sqlalchemy.sql import func



class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    content_type = db.Column(db.String(50))  # Ejemplo: 'text', 'image', 'video'
    image_url = db.Column(db.String(200), nullable=True)  # URL de la imagen
    video_url = db.Column(db.String(200), nullable=True)  # URL del video
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='publications')  # Relación con el usuario
    likes_count = db.Column(db.Integer, default=0)
