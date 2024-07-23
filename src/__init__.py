from flask import Flask

from src.config import Config
from src.views.main.routes import main_bp
from src.views.auth.routes import auth_bp
from src.views.artist.routes import artist_bp
from src.views.album.routes import album_bp
from src.views.track.routes import track_bp
from src.views.user.routes import user_bp
from src.extensions import login_manager, db, migrate, bcrypt, cache, sess
from src.commands import init_db
from src.models.models import User, Track

BLUEPRINTS = [main_bp ,auth_bp, artist_bp, album_bp, track_bp, user_bp]
COMMANDS = [init_db]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_blueprint(app)
    register_extensions(app)
    register_commands(app)

    return app


def register_extensions(app):
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    cache.init_app(app)
    sess.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

def register_blueprint(app):
    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)