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
