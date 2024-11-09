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
