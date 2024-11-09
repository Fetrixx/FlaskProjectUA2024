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
