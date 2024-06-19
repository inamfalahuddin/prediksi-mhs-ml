import hashlib
from app.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=True)
    updated_at = db.Column(db.DateTime(), nullable=True)
    is_active = db.Column(db.Boolean(), default=True)  # Atribut is_active

    def set_password(self, password):
        self.password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    def check_password(self, provided_password):
        hashed_password = hashlib.sha256(provided_password.encode('utf-8')).hexdigest()
        return hashed_password == self.password

    def get_id(self):
        return str(self.id)

    def load_user(user_id):
        return User.query.get(int(user_id))

    def get_by_id(user_id):
        return User.query.get(int(user_id))

    @property
    def is_authenticated(self):
        return True  # You can implement your authentication logic here
