from .. import db
from sqlalchemy.sql import func


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
