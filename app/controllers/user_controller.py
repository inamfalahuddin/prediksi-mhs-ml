from datetime import datetime
from app import db
from app.forms import CreateAcount
from app.models.user import User


def create_user():
    form = CreateAcount()

    new_user = User(username=form.username.data, email=form.email.data, role=form.role.data)
    new_user.set_password(form.password.data)
    new_user.created_at = datetime.utcnow()
    db.session.add(new_user)
    db.session.commit()


def edit_user(user_id):
    form = CreateAcount()

    user = User.get_by_id(user_id)
    user.username = form.username.data
    user.email = form.email.data
    user.role = form.role.data
    user.updated_at = datetime.utcnow()
    db.session.commit()


def delete_user(user_id):
    user = User.get_by_id(user_id)
    db.session.delete(user)
    db.session.commit()
