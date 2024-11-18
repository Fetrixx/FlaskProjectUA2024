# website/views/publication_views.py 

from flask import Blueprint, jsonify, redirect, render_template, request, flash, url_for
from flask_login import login_required, current_user

from website.models.like import Like
from website.models.publication import Publication
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
    playCuakSound = False
    user_id = current_user.id
    publication = Publication.query.get_or_404(publication_id)
    existing_like = Like.query.filter_by(user_id=user_id, publication_id=publication.id).first()

    if existing_like:
        db.session.delete(existing_like)
        publication.likes_count -= 1
        flash_message = "Has quitado tu 'me gusta'."
    else:
        playCuakSound = True
        new_like = Like(user_id=user_id, publication_id=publication.id)
        db.session.add(new_like)
        publication.likes_count += 1
        flash_message = "Has dado 'me gusta' a la publicación."

    db.session.commit()

    # Responder con un JSON
    response = {'likes_count': publication.likes_count, 'playCuakSound': playCuakSound, 'flash_message': flash_message}

    if request.is_json:  # Si la solicitud es AJAX (JSON)
        return jsonify(response), 200
    else:
        # Si no es AJAX, redirige con el mensaje flash adecuado
        flash(flash_message, category='info' if 'quitado' in flash_message else 'success')
        return redirect(url_for('publication_views.index'))


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
