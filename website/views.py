from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Note, User, Follow
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
        note = request.form.get('note')

        if len(note) < 1:
            flash('La nota es muy corta!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota agregada correctamente!', category='success')

    # Obtener las notas del usuario actual
    user_notes = current_user.notes
    # Obtener los IDs de los usuarios que el usuario actual está siguiendo
    followed_ids = {follow.followed_id for follow in current_user.followed}
    
    # Obtener las notas de los usuarios seguidos, excluyendo las del usuario actual
    followed_notes = Note.query.filter(Note.user_id.in_(followed_ids), Note.user_id != current_user.id).all()

    # Obtener la zona horaria local
    local_tz = get_localzone()

    # Convertir y formatear las fechas a la zona horaria local
    for note in followed_notes:
        note.date = note.date.astimezone(local_tz)  # Convierte a la zona horaria local

    return render_template("home.html", user=current_user, user_notes=user_notes, followed_notes=followed_notes)

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