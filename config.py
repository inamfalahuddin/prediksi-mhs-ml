import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'GASDF845@#$85!'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'mysql+mysqlconnector://root@localhost/prediksi_mhs_database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_NAME = os.environ.get('SERVER_NAME') or 'localhost:5000'
    SECRET_SALT = os.environ.get('SECRET_SALT') or 'GASDF845@#$85!'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    # UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
