from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import login_user

from app import db
from app.forms import RegistrationForm, LoginForm
from app.models.user import User


def register():
    form = RegistrationForm()

    new_user = User(username=form.username.data, email=form.email.data, role='user')
    new_user.set_password(form.password.data)
    new_user.created_at = datetime.utcnow()
    db.session.add(new_user)
    db.session.commit()
