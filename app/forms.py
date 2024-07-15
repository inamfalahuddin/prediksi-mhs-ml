from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange

from app.models.user import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Invalid email. Please try again.')


class CreateAcount(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('user', 'User')], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username does exist. Please unique username.')


class CreateMahasiswa(FlaskForm):
    npm = StringField('NPM', validators=[DataRequired()])
    nama = StringField('Nama', validators=[DataRequired()])
    prodi = StringField('Prodi', validators=[DataRequired()])
    ket_aktif = SelectField('Tahun Masuk', choices=[('AKTIF', 'Aktif'), ('NON AKTIF', 'Non Aktif')],
                            validators=[DataRequired()])
    tahun_masuk = IntegerField('Tahun Masuk',
                               validators=[DataRequired(), NumberRange(min=1900, max=datetime.now().year)])
    submit = SubmitField('Submit')

    def validate_npm(self, npm):
        user = User.query.filter_by(npm=npm.data).first()
        if user is not None:
            raise ValidationError('Nama does exist. Please unique npm.')


class CreateTranskip(FlaskForm):
    ips = FloatField('IPS', validators=[DataRequired()])
    sks = IntegerField('Sks', validators=[DataRequired()])
    submit = SubmitField('Submit')
