from datetime import datetime
from flask import flash, redirect, url_for
from app import db
from app.forms import CreateMahasiswa
from app.models.mahasiswa import Mahasiswa


def create_mahasiswa():
    form = CreateMahasiswa()

    existing_mahasiswa = Mahasiswa.query.filter_by(npm=form.npm.data).first()
    if existing_mahasiswa:
        flash('NPM sudah digunakan oleh mahasiswa lain.', 'error')
        return redirect(url_for('main.mahasiswa'))

    mahasiswa = Mahasiswa(
        npm=form.npm.data,
        nama=form.nama.data,
        prodi=form.prodi.data,
        tahun_masuk=form.tahun_masuk.data,
        ket_aktif=form.ket_aktif.data,
        created_at=datetime.utcnow()
    )

    result = mahasiswa.set_mahasiswa()

    flash('Your account has been created!', 'success')


def edit_mahasiswa(mahasiswa_id):
    form = CreateMahasiswa()

    mahasiswa = Mahasiswa.get_by_id(mahasiswa_id)
    existing_mahasiswa = Mahasiswa.query.filter(Mahasiswa.npm == form.npm.data).first()

    if existing_mahasiswa and existing_mahasiswa.id != mahasiswa_id:
        flash('NPM sudah digunakan oleh mahasiswa lain.', 'error')
        return redirect(url_for('main.dashboard'))

    mahasiswa.npm = form.npm.data
    mahasiswa.nama = form.nama.data
    mahasiswa.prodi = form.prodi.data
    mahasiswa.ket_aktif = form.ket_aktif.data
    mahasiswa.updated_at = datetime.now()
    db.session.commit()

    flash('Your account has been updated!', 'success')


def delete_mahasiswa(mahasiswa_id):
    mahasiswa = Mahasiswa.get_by_id(mahasiswa_id)
    db.session.delete(mahasiswa)
    db.session.commit()

    flash('Your account has been deleted!', 'success')
