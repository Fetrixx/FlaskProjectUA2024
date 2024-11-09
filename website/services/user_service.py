# website/services/user_service.py

from flask import flash
from flask_login import current_user
from .. import db
from ..models.user import User
from ..models.profile import Profile
from ..models.publication import Publication

def get_user_profile(user_id):
    """Obtiene el perfil de un usuario por ID"""
    user = User.query.get_or_404(user_id)
    followers_count = user.followers.count()
    following_count = user.followed.count()
    posts = Publication.query.filter_by(user_id=user.id).order_by(Publication.date.desc()).all()
    posts_count = len(posts)
    return user, followers_count, following_count, posts, posts_count

def update_user_profile(user_id, first_name, bio, background_picture):
    """Actualiza los datos de un usuario y su perfil"""
    user = User.query.get_or_404(user_id)
    profile = Profile.query.filter_by(user_id=user.id).first()
    
    if not profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
    
    user.first_name = first_name
    profile.bio = bio
    profile.background_picture = background_picture
    
    db.session.commit()

    return user, profile

def get_following_users():
    """Obtiene todos los usuarios que sigue el usuario actual"""
    following_users = current_user.followed.all()
    return following_users

def get_all_users(query=''):
    """Obtiene todos los usuarios y los filtra si se pasa una consulta"""
    all_users = User.query.all()
    followed_ids = {follow.followed_id for follow in current_user.followed}
    users = [user for user in all_users if user.id not in followed_ids and user.id != current_user.id]

    if query:
        query = query.lower()
        users = [
            user for user in users
            if query in user.first_name.lower() or
                query in user.username.lower() or
                query in user.email.lower()
        ]

    return users
