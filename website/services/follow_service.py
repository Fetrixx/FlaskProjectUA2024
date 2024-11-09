# website/services/follow_service.py

from flask import flash
from flask_login import current_user
from .. import db
from ..models.user import User
from ..models.follow import Follow

def follow_user(user_id):
    user_to_follow = User.query.get(user_id)
    if user_to_follow and user_to_follow != current_user:
        follow_entry = Follow(follower_id=current_user.id, followed_id=user_to_follow.id)
        db.session.add(follow_entry)
        db.session.commit()
        flash([f'Seguido a {user_to_follow.first_name} correctamente!'], category='success')
    else:
        flash(['No puedes seguirte a ti mismo o el usuario no existe.'], category='error')

def unfollow_user(user_id):
    follow_entry = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if follow_entry:
        db.session.delete(follow_entry)
        db.session.commit()
        flash(['Has dejado de seguir a este usuario.'], category='success')
    else:
        flash(['No estás siguiendo a este usuario.'], category='error')
