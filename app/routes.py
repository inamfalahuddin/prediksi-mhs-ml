import json
from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .forms import RegistrationForm, LoginForm, CreateAcount, CreateMahasiswa
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.controllers import user_controller, mahasiswa_controller, transkip_controller, prediksi_controller
from app.controllers import auth_controller
from .models.mahasiswa import Mahasiswa
from .models.transkip import Transkip

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # form = LoginForm()
    # return render_template('login.html', form=form)
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if form.validate_on_submit():
        auth_controller.register()
        flash('Your account has been created!', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)  # Mengirimkan form ke template


@main.route('/dashboard')
@login_required  # Hanya pengguna yang sudah login yang bisa mengakses dashboard
def dashboard():
    return render_template('dashboard.html')


@main.route('/logout')
def logout():
    logout_user()
    flash('Logout successful!', 'success')
    return redirect(url_for('main.index'))


@main.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    # user = User.query.filter_by(role='admin').all()
    user = User.query.all()
    header = ['No', 'Username', 'Email', 'Role', 'Created At']
    title = 'Data Admin'

    form = CreateAcount()

    return render_template('admin.html', data=user, header=header, title=title, form=form)


@main.route('/add_user', methods=['POST'])
@login_required
def add_user():
    user_controller.create_user()
    flash('Your account has been created!', 'success')
    return redirect(url_for('main.admin'))


@main.route('/edit_user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user_controller.edit_user(user_id)
    flash('Your account has been updated!', 'success')
    return redirect(url_for('main.admin'))


@main.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user_controller.delete_user(user_id)
    flash('Your account has been deleted!', 'success')
    return redirect(url_for('main.admin'))


@main.route('/mahasiswa', methods=['GET'])
@login_required
def mahasiswa():
    form = CreateMahasiswa()

    mahasiswa = Mahasiswa.query.all()
    header = ['No', 'NPM', 'Nama', 'Program Studi', 'Status', 'Created At']
    title = 'Data Mahasiswa'

    return render_template('mahasiswa.html', data=mahasiswa, header=header, title=title, form=form)


@main.route('/add_mahasiswa', methods=['POST'])
@login_required
def add_mahasiswa():
    mahasiswa_controller.create_mahasiswa()
    return redirect(url_for('main.mahasiswa'))


@main.route('/edit_mahasiswa/<int:mahasiswa_id>', methods=['POST'])
@login_required
def edit_mahasiswa(mahasiswa_id):
    mahasiswa_controller.edit_mahasiswa(mahasiswa_id)
    return redirect(url_for('main.mahasiswa'))


@main.route('/delete_mahasiswa/<int:mahasiswa_id>', methods=['POST'])
@login_required
def delete_mahasiswa(mahasiswa_id):
    mahasiswa_controller.delete_mahasiswa(mahasiswa_id)
    return redirect(url_for('main.mahasiswa'))


@main.route('/transkip', methods=['GET'])
@login_required
def transkip():
    form = CreateMahasiswa()

    mahasiswa = Mahasiswa.get_data_transkip()
    title = 'Data Mahasiswa'
    header = ['No', 'Nama Mahasiswa']

    if any('ips' in mhs and mhs['ips'] for mhs in mahasiswa):
        header = ['No', 'Nama Mahasiswa'] + ['IPS{}'.format(i + 1) for i in range(len(mahasiswa[0]['ips']))] + ['IPK',
                                                                                                                'SKS']
    return render_template('transkip.html', data=mahasiswa, header=header, title=title, form=form)


@main.route('/edit_transkip/<int:mahasiswa_id>', methods=['POST'])
@login_required
def edit_transkip(mahasiswa_id):
    transkip_controller.edit_transkip(mahasiswa_id)
    return redirect(url_for('main.transkip'))


@main.route('/prediksi', methods=['GET'])
@login_required
def prediksi():
    nama = request.args.get('nama')

    data = None

    if nama is not None:
        data = Mahasiswa.get_by_name(nama)

        for mhs in data:
            mhs.prediksi = prediksi_controller.prediksi_mahasiswa(mhs.id)

    return render_template('prediksi.html', data=data)


@main.route('/prediksi/<int:mahasiswa_id>', methods=['GET'])
def prediksi_exce(mahasiswa_id):
    prediksi_controller.prediksi_mahasiswa(mahasiswa_id)
    return 'Hlalo sayang'
