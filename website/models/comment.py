from .. import db
from sqlalchemy.sql import func



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
    