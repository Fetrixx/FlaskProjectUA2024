from flask import Blueprint, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from .models import Like, Profile, Publication, User, Follow, Comment, Message
from . import db
import json
from datetime import datetime
import pytz
from tzlocal import get_localzone


views = Blueprint('views', __name__)
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    playCuakSound = False
    if request.method == 'POST': 
        post_content = request.form.get('post')
        content_type = request.form.get('content_type')  # Obtener el tipo de contenido
        image_url = request.form.get('image_url')  # Obtener la URL de la imagen
        video_url = request.form.get('video_url')  # Obtener la URL del video

        # if len(post_content) > 0:
        if post_content and len(post_content) > 0:
            # Extraer ID del video si se proporciona una URL
            if content_type == 'video' and video_url:
                # Extraer ID del video de YouTube
                video_id = extract_video_id(video_url)
                if video_id:
                    new_post = Publication(
                        data=post_content,
                        user_id=current_user.id,
                        content_type=content_type,
                        image_url=image_url if content_type == 'image' else None,
                        video_url=f"https://www.youtube.com/embed/{video_id}"  # URL de incrustación
                    )
                else:
                    flash(['URL del video no válida.'], category='error')
                    return redirect(url_for('views.home'))
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
            playCuakSound = True
            flash(['Publicación agregada correctamente!'], category='success')
        else:
            flash(['La publicación es muy corta!'], category='error')

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


    return render_template("home.html", user=current_user, posts=all_posts, play_cuak=playCuakSound)


def extract_video_id(url):
    """Extrae el ID del video de una URL de YouTube."""
    if "youtu.be" in url:
        return url.split("/")[-1]
    elif "youtube.com/watch?v=" in url:
        return url.split("v=")[-1]
    return None


# Nueva ruta para seguir a un usuario
@views.route('/follow/<int:user_id>', methods=['POST', 'GET'])
@login_required
def follow(user_id):
    user_to_follow = User.query.get(user_id)
    if user_to_follow and user_to_follow != current_user:
        follow_entry = Follow(follower_id=current_user.id, followed_id=user_to_follow.id)
        db.session.add(follow_entry)
        db.session.commit()
        flash([f'Seguido a {user_to_follow.first_name} correctamente!'], category='success')
    else:
        flash(['No puedes seguirte a ti mismo o el usuario no existe.'], category='error')
    
    # Redirige a la página anterior o a la raíz en todos los casos
    return redirect(request.referrer or 'views.home')




# Ruta para dejar de seguir a un usuario
@views.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def unfollow(user_id):
    follow_entry = Follow.query.filter_by(follower_id=current_user.id, followed_id=user_id).first()
    if follow_entry:
        db.session.delete(follow_entry)
        db.session.commit()
        flash(['Has dejado de seguir a este usuario.'], category='success')
    else:
        flash(['No estás siguiendo a este usuario.'], category='error')

    return redirect(request.referrer or 'views.home')



@views.route('/comment/<int:publication_id>', methods=['POST'])
@login_required
def comment(publication_id):
    comment_content = request.form.get('comment')
    parent_comment_id = request.form.get('parent_id')  # Puede ser None si es un nuevo comentario

    print(f"Comentario: {comment_content}, Parent ID: {parent_comment_id}")  # Para depuración

    if len(comment_content) < 1:
        flash(['El comentario es muy corto!'], category='error')
    else:
        new_comment = Comment(data=comment_content, user_id=current_user.id, publication_id=publication_id, parent_id=parent_comment_id)
        db.session.add(new_comment)
        db.session.commit()
        flash(['Comentario agregado correctamente!'], category='success')

    return redirect(url_for('views.home'))

@views.route('/delete-comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if comment and comment.user_id == current_user.id:
        db.session.delete(comment)
        db.session.commit()
        flash(['Comentario eliminado correctamente!'], category='success')
    else:
        flash(['No puedes eliminar este comentario.'], category='error')
    
    return redirect(url_for('views.home'))

@views.route('/delete-publication/<int:publication_id>', methods=['POST'])
@login_required
def delete_publication(publication_id):
    publication = Publication.query.get(publication_id)
    if publication and publication.user_id == current_user.id:
        db.session.delete(publication)
        db.session.commit()
        flash(['Publicación eliminada correctamente!'], category='success')
    else:
        flash(['No puedes eliminar esta publicación.'], category='error')

    return redirect(url_for('views.home'))


# Nueva ruta para ver a quién sigue el usuario
@views.route('/my-following', methods=['GET'])
@login_required
def my_following():
    query = request.args.get('query', '')
    following_users = current_user.followed.all()

    # Filtrar usuarios según la búsqueda
    if query:
        following_users = [follow for follow in following_users if query.lower() in follow.followed_user.first_name.lower() or query.lower() in follow.followed_user.email.lower()]

    return render_template('my_following.html', following=following_users, user=current_user, query=query)


# Nueva ruta para ver todos los usuarios
@views.route('/users', methods=['GET'])
@login_required
def user_list():
    query = request.args.get('query', '')
    
    # Obtener todos los usuarios
    all_users = User.query.all()
    
    # Obtener los IDs de los usuarios que el usuario actual está siguiendo
    followed_ids = {follow.followed_id for follow in current_user.followed}
    
    # Filtrar solo los usuarios que no están siendo seguidos y que no son el usuario actual
    users = [user for user in all_users if user.id not in followed_ids and user.id != current_user.id]

    # Filtrar usuarios según la búsqueda
    if query:
        users = [user for user in users if query.lower() in user.first_name.lower() or query.lower() in user.email.lower()]

    return render_template('user_list.html', users=users, user=current_user, query=query)

@views.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile(user_id):
    playCuakSound = False
    user = User.query.get_or_404(user_id)  # Obtener el usuario o lanzar un error 404
    followers_count = user.followers.count()  # Contar seguidores
    following_count = user.followed.count()  # Contar seguidos
    posts = Publication.query.filter_by(user_id=user.id).order_by(Publication.date.desc()).all()  # Obtener posts del usuario
    posts_count = len(posts)  # Contar publicaciones

    is_current_user = (current_user.id == user.id)  # Verificar si es el perfil del usuario actual
    is_following = current_user.id in [follow.follower_id for follow in user.followers]  # Verificar si está siguiendo

    playCuakSound = True
    return render_template('profile.html', user=user, followers_count=followers_count,
                           following_count=following_count, posts=posts,
                           posts_count=posts_count, is_current_user=is_current_user,
                           is_following=is_following, play_cuak=playCuakSound)


@views.route('/edit-profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_profile(user_id):
    playCuakSound = False
    user = User.query.get_or_404(user_id)

    # Verificar si el usuario que intenta editar es el usuario actual
    if user.id != current_user.id:
        flash(['No tienes permiso para editar este perfil.'], category='error')
        return redirect(url_for('views.home'))

    # Cargar el perfil del usuario
    profile = Profile.query.filter_by(user_id=user.id).first()
    if not profile:
        # Crear un perfil si no existe
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()


    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        bio = request.form.get('bio')
        background_picture = request.form.get('background_picture')
        
            
        # Imprimir datos antes de la edición
        print("Datos del usuario antes de la edición:")
        print("Username:", user.username)
        print("name:", user.first_name)
        print("Bio:", profile.bio)
        print("Profile Picture:", user.profile_picture)
        print("Background Picture:", profile.background_picture)

        # Actualizar datos
        # user.username = username
        user.first_name = first_name
        profile.bio = bio
        profile.background_picture = background_picture

        db.session.commit()

        # Imprimir datos después de la edición
        print("Datos del usuario después de la edición:")
        print("Username:", user.username)
        print("name:", user.first_name)
        print("Bio:", profile.bio)
        print("Profile Picture:", user.profile_picture)
        print("Background Picture:", profile.background_picture)

        playCuakSound = True
        flash(['Perfil actualizado correctamente!'], category='success')
        return redirect(url_for('views.profile', user_id=user.id, play_cuak=playCuakSound))

    return render_template('edit_profile.html', user=user, profile=profile, play_cuak=playCuakSound)




@views.route('/like/<int:publication_id>', methods=['POST'])
@login_required
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
    return redirect(request.referrer or url_for('views.home'))

@views.route('/like-comment/<int:comment_id>', methods=['POST'])
@login_required
def like_comment(comment_id):
    playCuakSound = False
    comment = Comment.query.get(comment_id)
    if not comment:
        flash(['Comentario no encontrado.'], category='error')
        return redirect(url_for('views.home'))

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
    return redirect(url_for('views.home', play_cuak=playCuakSound))


@views.route('/post/<int:post_id>', methods=['GET'])
@login_required
def view_post(post_id):
    individual_post = Publication.query.get_or_404(post_id)
    
    individual_post.liked = Like.query.filter_by(user_id=current_user.id, publication_id=individual_post.id).first() is not None
    individual_post.likes_count = Like.query.filter_by(publication_id=individual_post.id).count()
    
    individual_post.comments = Comment.query.filter_by(publication_id=individual_post.id).all()
    for comment in individual_post.comments:
        comment.liked = Like.query.filter_by(user_id=current_user.id, comment_id=comment.id).first() is not None
        comment.likes_count = Like.query.filter_by(comment_id=comment.id).count()


    return render_template("view_post.html", user=current_user, _publication=individual_post)


def send_message(sender_id, receiver_id, content):
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()





def get_messages(user_id, other_user_id):
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.timestamp).all()
    return messages



@views.route('/messages')
def mensajes():
    # Obtener los usuarios seguidos por el usuario actual
    followed_users = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == current_user.id).all()

    # Obtener los mensajes entre el usuario actual y los usuarios seguidos
    messages = []
    for user in followed_users:
        user_messages = get_messages(current_user.id, user.id)  # Obtener mensajes entre el usuario actual y el seguido
        messages.append((user, user_messages))

    return render_template('messages.html', followed_users=followed_users, messages=messages, user=current_user)


@views.route('/get_messages/<int:other_user_id>', methods=['GET'])
def get_messages_route(other_user_id):
    user_id = current_user.id  # Asumiendo que estás utilizando Flask-Login
    messages = get_messages(user_id, other_user_id)
    
    # Añadir datos del usuario que envió el mensaje
    users = {
        user.id: {'first_name': user.first_name, 'username': user.username}
        for user in [current_user, User.query.get(other_user_id)]
    }

    # Retorna los mensajes en formato JSON
    return jsonify([{
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'sender_first_name': users[message.sender_id]['first_name'],
        'sender_username': users[message.sender_id]['username'],
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in messages])


@views.route('/send_message', methods=['POST'])
def send_message_route():
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    sender_id = current_user.id  # Asumiendo que estás usando Flask-Login
    
    send_message(sender_id, receiver_id, content)
    return jsonify({"message": "Mensaje enviado con éxito"})




@views.route('/edit-publication/<int:publication_id>', methods=['POST'])
@login_required
def edit_publication(publication_id):
    publication = Publication.query.get(publication_id)
    if publication and publication.user_id == current_user.id:
        new_content = request.form.get('post')
        image_url = request.form.get('image_url')
        video_url = request.form.get('video_url')
        content_type = request.form.get('content_type')
        
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
    
    return redirect(url_for('views.home'))

@views.route('/edit-comment/<int:comment_id>', methods=['POST'])
@login_required
def edit_comment(comment_id):
    # Buscar el comentario en la base de datos por su ID
    comment = Comment.query.get(comment_id)
    
    # Verificar si el comentario existe y si el usuario es el propietario
    if comment and comment.user_id == current_user.id:
        # Obtener el nuevo contenido del comentario del formulario
        new_comment_content = request.form.get('comment')
        
        # Verificar si el contenido no está vacío
        if len(new_comment_content) > 0:
            # Actualizar el contenido del comentario
            comment.data = new_comment_content
            db.session.commit()  # Guardar los cambios en la base de datos
            
            # Mostrar un mensaje de éxito
            flash(['Comentario editado correctamente!'], category='success')
        else:
            # Si el comentario está vacío o es demasiado corto
            flash(['El comentario es muy corto!'], category='error')
    else:
        # Si el comentario no existe o el usuario no tiene permisos para editarlo
        flash(['No tienes permiso para editar este comentario.'], category='error')

    # Redirigir al usuario a la página de inicio o la página de detalle de la publicación
    return redirect(url_for('views.home'))

