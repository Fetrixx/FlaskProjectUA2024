from .comment_views import comment_views
from .follow_views import follow_views
from .home_views import home_views
from .messages_views import messages_views
from .publication_views import publication_views
from .user_views import user_views
from ..controllers.auth_controller import auth

def register_blueprints(app):
    app.register_blueprint(home_views)
    app.register_blueprint(follow_views)
    app.register_blueprint(comment_views)
    app.register_blueprint(user_views)
    app.register_blueprint(messages_views)
    app.register_blueprint(publication_views)
    
    app.register_blueprint(auth, url_prefix="/")