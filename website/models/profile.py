from .. import db


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)  # Relación uno a uno
    bio = db.Column(db.Text)  # Biografía
    background_picture = db.Column(db.String(200), default='https://media.istockphoto.com/id/1223483739/vector/seamless-pattern-with-user-experience-icons.jpg?s=612x612&w=0&k=20&c=AYDPQuJQVAKoVjl8qYDP4C53ZvmZXGIwPhJpquB6gus=')  # URL de la imagen de perfil por defecto

    # user = db.relationship('User', backref='profile')  # Relación inversa
