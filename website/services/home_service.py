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
