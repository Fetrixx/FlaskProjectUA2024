# website/services/messages_service.py

from .. import db
from ..models.message import Message
from ..models.user import User
from ..models.follow import Follow

def get_followed_users(user_id):
    # Obtener los usuarios seguidos por el usuario actual
    followed_users = User.query.join(Follow, Follow.followed_id == User.id).filter(Follow.follower_id == user_id).all()
    return followed_users

def get_messages(user_id, other_user_id):
    # Obtener los mensajes entre el usuario actual y el usuario seguido
    messages = Message.query.filter(
        ((Message.sender_id == user_id) & (Message.receiver_id == other_user_id)) |
        ((Message.sender_id == other_user_id) & (Message.receiver_id == user_id))
    ).order_by(Message.timestamp).all()
    return messages

def send_message(sender_id, receiver_id, content):
    # Enviar un nuevo mensaje
    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
    db.session.add(new_message)
    db.session.commit()

def get_user_info(user_ids):
    # Obtener la información de los usuarios (nombre, username) a partir de sus IDs
    users = {user.id: {'first_name': user.first_name, 'username': user.username} for user in User.query.filter(User.id.in_(user_ids)).all()}
    return users
