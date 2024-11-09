# website/views/user_views.py

from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from ..services.user_service import get_user_profile, update_user_profile, get_following_users, get_all_users
from ..models.user import User

user_views = Blueprint('user_views', __name__)

@user_views.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile(user_id):
    playCuakSound = False
    user, followers_count, following_count, posts, posts_count = get_user_profile(user_id)

    is_current_user = (current_user.id == user.id)
    is_following = current_user.id in [follow.follower_id for follow in user.followers]

    playCuakSound = True
    return render_template('profile.html', user=user, followers_count=followers_count,
                           following_count=following_count, posts=posts,
                           posts_count=posts_count, is_current_user=is_current_user,
                           is_following=is_following, play_cuak=playCuakSound)

@user_views.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    playCuakSound = False
    user = User.query.get_or_404(user_id)

    if user.id != current_user.id:
        flash(['No tienes permiso para editar este perfil.'], category='error')
        return redirect(url_for('home_views.home'))

    profile = user.profile  # Obtiene el perfil directamente desde el usuario

    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        bio = request.form.get('bio')
        background_picture = request.form.get('background_picture')

        print("Datos del usuario antes de la edición:")
        print("Username:", user.username)
        print("Name:", user.first_name)
        print("Bio:", profile.bio)
        print("Profile Picture:", user.profile_picture)
        print("Background Picture:", profile.background_picture)

        user, profile = update_user_profile(user.id, first_name, bio, background_picture)

        print("Datos del usuario después de la edición:")
        print("Username:", user.username)
        print("Name:", user.first_name)
        print("Bio:", profile.bio)
        print("Profile Picture:", user.profile_picture)
        print("Background Picture:", profile.background_picture)

        playCuakSound = True
        flash(['Perfil actualizado correctamente!'], category='success')
        return redirect(url_for('user_views.profile', user_id=user.id, play_cuak=playCuakSound))

    return render_template('edit_profile.html', user=user, profile=profile, play_cuak=playCuakSound)

@user_views.route('/my-following', methods=['GET'])
@login_required
def my_following():
    query = request.args.get('query', '')
    following_users = get_following_users()

    if query:
        following_users = [
            follow for follow in following_users
            if query.lower() in follow.followed_user.first_name.lower() or
            query.lower() in follow.followed_user.username.lower() or
            query.lower() in follow.followed_user.email.lower()]

    return render_template('my_following.html', following=following_users, user=current_user, query=query)

@user_views.route('/users', methods=['GET'])
@login_required
def user_list():
    query = request.args.get('query', '').lower()
    users = get_all_users(query)


    if query:
        users = [
            user for user in users
            if query in user.first_name.lower() or
               query in user.username.lower() or
               query in user.email.lower()
        ]
        
    return render_template('user_list.html', users=users, user=current_user, query=query)
