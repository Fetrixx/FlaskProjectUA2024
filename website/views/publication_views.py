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
