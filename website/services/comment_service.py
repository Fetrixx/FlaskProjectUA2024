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
