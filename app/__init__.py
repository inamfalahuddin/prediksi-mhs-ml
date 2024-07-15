from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from .extensions import db
from app.models.user import User  # Pastikan impor ini benar


def create_app():
    app = Flask(__name__, static_url_path='/static')
    app.config.from_object(Config)

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
