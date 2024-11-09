# website/views/comment_views.py

from flask import Blueprint, redirect, request, flash, url_for
from flask_login import login_required, current_user
from ..services.comment_service import add_comment, delete_comment, like_comment, edit_comment

comment_views = Blueprint('comment_views', __name__)

@comment_views.route('/comment/<int:publication_id>', methods=['POST'])
@login_required
def comment(publication_id):
    comment_content = request.form.get('comment')
    parent_comment_id = request.form.get('parent_id')  # Puede ser None si es un nuevo comentario

    print(f"Comentario: {comment_content}, Parent ID: {parent_comment_id}")  # Para depuración

    new_comment = add_comment(publication_id, comment_content, parent_comment_id)
    if new_comment is None:
        return redirect(url_for('home_views.home'))  # Si no se agrega el comentario, redirige

    return redirect(url_for('home_views.home'))

@comment_views.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment_route(comment_id):
    delete_comment(comment_id)
    return redirect(url_for('home_views.home'))

@comment_views.route('/like-comment/<int:comment_id>', methods=['POST'])
@login_required
def like_comment_route(comment_id):
    success, play_cuak_sound = like_comment(comment_id)
    return redirect(url_for('home_views.home', play_cuak=play_cuak_sound))

@comment_views.route('/edit-comment/<int:comment_id>', methods=['POST'])
@login_required
def edit_comment_route(comment_id):
    new_comment_content = request.form.get('comment')
    edit_comment(comment_id, new_comment_content)
    return redirect(url_for('home_views.home'))
