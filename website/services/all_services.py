# website/services/comment_service.py

from flask import flash
from flask_login import current_user
from .. import db
from ..models.comment import Comment
from ..models.like import Like

def add_comment(publication_id, comment_content, parent_comment_id=None):
    if len(comment_content) < 1:
        flash(['El comentario es muy corto!'], category='error')
        return None

    new_comment = Comment(data=comment_content, user_id=current_user.id, publication_id=publication_id, parent_id=parent_comment_id)
    db.session.add(new_comment)
    db.session.commit()
    flash(['Comentario agregado correctamente!'], category='success')
    return new_comment

def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment and comment.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash(['Comentario eliminado correctamente!'], category='success')
    else:
        flash(['No puedes eliminar este comentario.'], category='error')

def like_comment(comment_id):
    playCuakSound = False
    comment = Comment.query.get(comment_id)
    if not comment:
        flash(['Comentario no encontrado.'], category='error')
        return False, playCuakSound

    like = Like.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
    if like:
        db.session.delete(like)
        flash(['Me gusta eliminado del comentario'], category='success')
    else:
        new_like = Like(user_id=current_user.id, comment_id=comment_id)
        db.session.add(new_like)
        playCuakSound = True
        flash(['Te gusta el comentario!'], category='success')

    db.session.commit()
    return True, playCuakSound

def edit_comment(comment_id, new_comment_content):
    comment = Comment.query.get(comment_id)

    if comment and comment.user_id == current_user.id:
        if len(new_comment_content) > 0:
            comment.data = new_comment_content
            db.session.commit()
            flash(['Comentario editado correctamente!'], category='success')
        else:
            flash(['El comentario es muy corto!'], category='error')
    else:
        flash(['No tienes permiso para editar este comentario.'], category='error')


# website/services/comment_service.py

from flask import flash
from flask_login import current_user
from .. import db
from ..models.comment import Comment
from ..models.like import Like

def add_comment(publication_id, comment_content, parent_comment_id=None):
    if len(comment_content) < 1:
        flash(['El comentario es muy corto!'], category='error')
        return None

    new_comment = Comment(data=comment_content, user_id=current_user.id, publication_id=publication_id, parent_id=parent_comment_id)
    db.session.add(new_comment)
    db.session.commit()
    flash(['Comentario agregado correctamente!'], category='success')
    return new_comment

def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment and comment.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash(['Comentario eliminado correctamente!'], category='success')
    else:
        flash(['No puedes eliminar este comentario.'], category='error')

def like_comment(comment_id):
    playCuakSound = False
    comment = Comment.query.get(comment_id)
    if not comment:
        flash(['Comentario no encontrado.'], category='error')
        return False, playCuakSound

    like = Like.query.filter_by(user_id=current_user.id, comment_id=comment_id).first()
    if like:
        db.session.delete(like)
        flash(['Me gusta eliminado del comentario'], category='success')
    else:
        new_like = Like(user_id=current_user.id, comment_id=comment_id)
        db.session.add(new_like)
        playCuakSound = True
        flash(['Te gusta el comentario!'], category='success')

    db.session.commit()
    return True, playCuakSound

def edit_comment(comment_id, new_comment_content):
    comment = Comment.query.get(comment_id)

    if comment and comment.user_id == current_user.id:
        if len(new_comment_content) > 0:
            comment.data = new_comment_content
            db.session.commit()
            flash(['Comentario editado correctamente!'], category='success')
        else:
            flash(['El comentario es muy corto!'], category='error')
    else:
        flash(['No tienes permiso para editar este comentario.'], category='error')


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


# website/services/home_service.py

from flask import flash
from flask_login import current_user
from .. import db
from ..models.publication import Publication
from ..models.like import Like
from ..models.comment import Comment
from .utils import extract_video_id

def create_post(post_content, content_type, image_url, video_url):
    play_cuak_sound = False
    
    if post_content and len(post_content) > 0:
        if content_type == 'video' and video_url:
            video_id = extract_video_id(video_url)
            if video_id:
                new_post = Publication(
                    data=post_content,
                    user_id=current_user.id,
                    content_type=content_type,
                    image_url=image_url if content_type == 'image' else None,
                    video_url=f"https://www.youtube.com/embed/{video_id}"
                )
            else:
                flash(['URL del video no válida.'], category='error')
                return None, play_cuak_sound
        else:
            new_post = Publication(
                data=post_content,
                user_id=current_user.id,
                content_type=content_type,
                image_url=image_url if content_type == 'image' else None,
                video_url=None
            )
        
        db.session.add(new_post)
        db.session.commit()
        play_cuak_sound = True
        flash(['Publicación agregada correctamente!'], category='success')
        return new_post, play_cuak_sound
    else:
        flash(['La publicación es muy corta!'], category='error')
        return None, play_cuak_sound

def load_user_posts():
    followed_ids = {follow.followed_id for follow in current_user.followed}
    all_posts = Publication.query.filter(Publication.user_id.in_(followed_ids.union({current_user.id}))).order_by(Publication.date.desc()).all()

    # Cargar todos los comentarios asociados a las publicaciones
    for post in all_posts:
        post.liked = Like.query.filter_by(user_id=current_user.id, publication_id=post.id).first() is not None
        post.likes_count = Like.query.filter_by(publication_id=post.id).count()

        post.comments = Comment.query.filter_by(publication_id=post.id).all()
        for comment in post.comments:
            comment.liked = Like.query.filter_by(user_id=current_user.id, comment_id=comment.id).first() is not None
            comment.likes_count = Like.query.filter_by(comment_id=comment.id).count()

    return all_posts


# website/services/messages_service.py

from .. import db
from ..models.message import Message
from ..models.user import User
from ..models.follow import Follow

def get_followed_users(user_id):
    # Obtener los usuarios seguidos por el usuario actual
    followed_users = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    return followed_users

def get_messages(user_id, other_user_id):
    # Obtener los mensajes entre el usuario actual y el usuario seguido
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.timestamp).all()
    return messages

def send_message(sender_id, receiver_id, content):
    # Enviar un nuevo mensaje
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()

def get_user_info(user_ids):
    # Obtener la información de los usuarios (nombre, username) a partir de sus IDs
    users = {user.id: {'first_name': user.first_name, 'username': user.username} for user in User.query.filter(User.id.in_(user_ids)).all()}
    return users



from flask import flash
from flask_login import current_user
from .. import db
from ..models.publication import Publication
from ..models.like import Like
from ..models.comment import Comment
from ..models.message import Message

def delete_publication(publication_id):
    publication = Publication.query.get(publication_id)
    if publication and publication.user_id == current_user.id:
        db.session.delete(publication)
        db.session.commit()
        flash(['Publicación eliminada correctamente!'], category='success')
    else:
        flash(['No puedes eliminar esta publicación.'], category='error')

def like_publication(publication_id):
    playCuakSound = False
    publication = Publication.query.get_or_404(publication_id)
    existing_like = Like.query.filter_by(user_id=current_user.id, publication_id=publication.id).first()

    if existing_like:
        db.session.delete(existing_like)
        publication.likes_count -= 1
        flash(['Has quitado tu "me gusta".'], category='info')
    else:
        playCuakSound = True
        new_like = Like(user_id=current_user.id, publication_id=publication.id)
        db.session.add(new_like)
        publication.likes_count += 1
        flash(['Has dado "me gusta" a la publicación.'], category='success')

    db.session.commit()
    return playCuakSound

def edit_publication(publication_id, new_content, image_url, video_url, content_type):
    publication = Publication.query.get(publication_id)
    if publication and publication.user_id == current_user.id:
        if len(new_content) > 0:
            publication.data = new_content
            publication.content_type = content_type
            publication.image_url = image_url if content_type == 'image' else None
            publication.video_url = video_url if content_type == 'video' else None
            db.session.commit()
            flash(['Publicación editada correctamente!'], category='success')
        else:
            flash(['La publicación es muy corta!'], category='error')
    else:
        flash(['No tienes permiso para editar esta publicación.'], category='error')

def send_message(sender_id, receiver_id, content):
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()

def get_publication_with_details(publication_id):
    publication = Publication.query.get_or_404(publication_id)
    publication.liked = Like.query.filter_by(user_id=current_user.id, publication_id=publication.id).first() is not None
    publication.likes_count = Like.query.filter_by(publication_id=publication.id).count()

    publication.comments = Comment.query.filter_by(publication_id=publication.id).all()
    for comment in publication.comments:
        comment.liked = Like.query.filter_by(user_id=current_user.id, comment_id=comment.id).first() is not None
        comment.likes_count = Like.query.filter_by(comment_id=comment.id).count()

    return publication




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
