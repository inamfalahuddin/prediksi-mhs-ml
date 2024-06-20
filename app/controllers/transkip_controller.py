from flask import flash, request
from app import db
from app.models.transkip import Transkip


def edit_transkip(mahasiswa_id):
    for i in range(1, 8):
        ips_key = f'ips_{i}_{mahasiswa_id}'
        sks_key = f'sks_{i}_{mahasiswa_id}'
        semester = f'Semester {i}'

        ips_value = request.form.get(ips_key)
        sks_value = request.form.get(sks_key)

        if ips_value and sks_value:
            # Cari data nilai berdasarkan mahasiswa_id dan semester
            nilai = Transkip.query.filter_by(mahasiswa_id=mahasiswa_id, semester=semester).first()
            if nilai:
                nilai.ips = float(ips_value)
                nilai.sks = int(sks_value)
            else:
                # Buat entri baru jika tidak ditemukan
                nilai = Transkip(mahasiswa_id=mahasiswa_id, semester=semester, ips=float(ips_value),
                                 sks=int(sks_value))
                db.session.add(nilai)

        db.session.commit()
    flash('Your transkip has been updated!', 'success')
