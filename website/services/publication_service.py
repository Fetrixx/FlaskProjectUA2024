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
