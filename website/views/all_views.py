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


# website/views/follow_views.py

from flask import Blueprint, redirect, request, flash, url_for
from flask_login import login_required, current_user
from ..services.follow_service import follow_user, unfollow_user

follow_views = Blueprint('follow_views', __name__)

# Nueva ruta para seguir a un usuario
@follow_views.route('/follow/<int:user_id>', methods=['POST', 'GET'])
@login_required
def follow_route(user_id):
    follow_user(user_id)
    return redirect(request.referrer or 'home_views.home')

# Ruta para dejar de seguir a un usuario
@follow_views.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow_route(user_id):
    unfollow_user(user_id)
    return redirect(request.referrer or 'home_views.home')


# website/views/home_views.py

from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from ..services.home_service import create_post, load_user_posts

home_views = Blueprint('home_views', __name__)

@home_views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    playCuakSound = False
    if request.method == 'POST': 
        post_content = request.form.get('post')
        content_type = request.form.get('content_type')  # Obtener el tipo de contenido
        image_url = request.form.get('image_url')  # Obtener la URL de la imagen
        video_url = request.form.get('video_url')  # Obtener la URL del video

        # Llamamos a la función del servicio para crear la publicación
        new_post, playCuakSound = create_post(post_content, content_type, image_url, video_url)

        if not new_post:
            return redirect(url_for('home_views.home'))  # Si no se crea la publicación, redirigimos de vuelta

    # Llamamos a la función del servicio para cargar las publicaciones
    all_posts = load_user_posts()

    return render_template("home.html", user=current_user, posts=all_posts, play_cuak=playCuakSound)

# website/views/messages_views.py

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from ..services.messages_service import get_followed_users, get_messages, send_message, get_user_info

messages_views = Blueprint('messages_views', __name__)

@messages_views.route('/messages')
@login_required
def mensajes():
    # Obtener los usuarios seguidos por el usuario actual
    followed_users = get_followed_users(current_user.id)

    # Obtener los mensajes entre el usuario actual y los usuarios seguidos
    messages = []
    for user in followed_users:
        user_messages = get_messages(current_user.id, user.id)  # Obtener mensajes entre el usuario actual y el seguido
        messages.append((user, user_messages))

    return render_template('messages.html', followed_users=followed_users, messages=messages, user=current_user)


@messages_views.route('/get_messages/<int:other_user_id>', methods=['GET'])
@login_required
def get_messages_route(other_user_id):
    user_id = current_user.id  # Asumiendo que estás utilizando Flask-Login
    messages = get_messages(user_id, other_user_id)
    
    # Obtener información de los usuarios (nombre y username)
    users = get_user_info([user_id, other_user_id])

    # Retorna los mensajes en formato JSON
    return jsonify([{
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'sender_first_name': users[message.sender_id]['first_name'],
        'sender_username': users[message.sender_id]['username'],
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages])


@messages_views.route('/send_message', methods=['POST'])
@login_required
def send_message_route():
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    sender_id = current_user.id  # Asumiendo que estás usando Flask-Login
    
    send_message(sender_id, receiver_id, content)
    return jsonify({"message": "Mensaje enviado con éxito"})


# website/views/publication_views.py 

from flask import Blueprint, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user
from .. import db
from ..services.publication_service import delete_publication, like_publication, edit_publication, send_message, get_publication_with_details

publication_views = Blueprint('publication_views', __name__)

@publication_views.route('/delete-publication/<int:publication_id>', methods=['POST'])
@login_required
def delete_publication_route(publication_id):
    delete_publication(publication_id)
    return redirect(url_for('home_views.home'))


@publication_views.route('/like/<int:publication_id>', methods=['POST'])
@login_required
def like_publication_route(publication_id):
    playCuakSound = like_publication(publication_id)
    return redirect(request.referrer or url_for('home_views.home', play_cuak=playCuakSound))


@publication_views.route('/post/<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    individual_post = get_publication_with_details(post_id)
    return render_template("view_post.html", user=current_user, _publication=individual_post)


@publication_views.route('/edit-publication/<int:publication_id>', methods=['POST'])
@login_required
def edit_publication_route(publication_id):
    new_content = request.form.get('post')
    image_url = request.form.get('image_url')
    video_url = request.form.get('video_url')
    content_type = request.form.get('content_type')

    edit_publication(publication_id, new_content, image_url, video_url, content_type)
    return redirect(url_for('home_views.home'))


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
