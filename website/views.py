from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, Publication, User, Follow, Comment
from . import db
import json
from datetime import datetime
import pytz
from tzlocal import get_localzone


views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        post_content = request.form.get('post')

        if len(post_content) < 1:
            flash('La publicación es muy corta!', category='error') 
        else:
            new_post = Publication(data=post_content, user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash('Publicación agregada correctamente!', category='success')

    followed_ids = {follow.followed_id for follow in current_user.followed}
    
    all_posts = Publication.query.filter(Publication.user_id.in_(followed_ids.union({current_user.id}))).order_by(Publication.date.desc()).all()

    # Aquí puedes cargar todos los comentarios asociados a las publicaciones
    for post in all_posts:
        post.comments = Comment.query.filter_by(publication_id=post.id).all()  # Cargar todos los comentarios de la publicación

    return render_template("home.html", user=current_user, posts=all_posts)

@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

# Nueva ruta para seguir a un usuario
@views.route('/follow/<int:user_id>')
@login_required
def follow(user_id):
    user_to_follow = User.query.get(user_id)
    if user_to_follow and user_to_follow != current_user:
        follow_entry = Follow(follower_id=current_user.id, followed_id=user_to_follow.id)
        db.session.add(follow_entry)
        db.session.commit()
        flash(f'Seguido a {user_to_follow.first_name} correctamente!', category='success')
    else:
        flash('No puedes seguirte a ti mismo o el usuario no existe.', category='error')
    
    return redirect('/')

@views.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    follow_entry = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if follow_entry:
        db.session.delete(follow_entry)
        db.session.commit()
        flash('Has dejado de seguir a este usuario.', category='success')
    else:
        flash('No estás siguiendo a este usuario.', category='error')

    return redirect(url_for('views.my_following'))

# Nueva ruta para ver a quién sigue el usuario
@views.route('/my-following')
@login_required
def my_following():
    following_users = current_user.followed.all()
    return render_template('my_following.html', following=following_users, user=current_user)  # Asegúrate de pasar 'user=current_user'

# Nueva ruta para ver todos los usuarios
@views.route('/users')
@login_required
def user_list():
    # Obtener todos los usuarios
    all_users = User.query.all()
    # Obtener los IDs de los usuarios que el usuario actual está siguiendo
    followed_ids = {follow.followed_id for follow in current_user.followed}
    # Filtrar solo los usuarios que no están siendo seguidos y que no son el usuario actual
    users = [user for user in all_users if user.id not in followed_ids and user.id != current_user.id]
    
    return render_template('user_list.html', users=users, user=current_user)

@views.route('/comment/<int:publication_id>', methods=['POST'])
@login_required
def comment(publication_id):
    comment_content = request.form.get('comment')
    parent_comment_id = request.form.get('parent_id')  # Puede ser None si es un nuevo comentario

    print(f"Comentario: {comment_content}, Parent ID: {parent_comment_id}")  # Para depuración

    if len(comment_content) < 1:
        flash('El comentario es muy corto!', category='error')
    else:
        new_comment = Comment(data=comment_content, user_id=current_user.id, publication_id=publication_id, parent_id=parent_comment_id)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comentario agregado correctamente!', category='success')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment and comment.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash('Comentario eliminado correctamente!', category='success')
    else:
        flash('No puedes eliminar este comentario.', category='error')
    
    return redirect(url_for('views.home'))

@views.route('/delete-publication/<int:publication_id>', methods=['POST'])
@login_required
def delete_publication(publication_id):
    publication = Publication.query.get(publication_id)
    if publication and publication.user_id == current_user.id:
        db.session.delete(publication)
        db.session.commit()
        flash('Publicación eliminada correctamente!', category='success')
    else:
        flash('No puedes eliminar esta publicación.', category='error')
    
    return redirect(url_for('views.home'))