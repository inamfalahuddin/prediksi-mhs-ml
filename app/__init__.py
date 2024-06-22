import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from .extensions import db
from app.models.user import User


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)
    migrate = Migrate(app, db)

    login_manager = LoginManager(app)
    login_manager.login_view = 'main.login'  # Atur view login yang digunakan oleh Flask-Login

    # Fungsi user_loader untuk memuat pengguna berdasarkan ID pengguna
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    return app
