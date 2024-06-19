import hashlib
from datetime import datetime

from app.extensions import db
from app.models.transkip import Transkip


class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    id = db.Column(db.Integer, primary_key=True)
    npm = db.Column(db.String(255), unique=False, nullable=True)
    nama = db.Column(db.String(255))
    prodi = db.Column(db.String(255))
    tahun_masuk = db.Column(db.String(255), nullable=True)
    ket_aktif = db.Column(db.String(255), nullable=True)
    ket_lulus = db.Column(db.String(255), nullable=True)
    total_sks = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    transkips = db.relationship('Transkip', backref='mahasiswa', lazy=True)

    def __init__(self, npm, nama, prodi, tahun_masuk, ket_aktif, created_at):
        self.npm = npm
        self.nama = nama
        self.prodi = prodi
        self.tahun_masuk = tahun_masuk
        self.ket_aktif = ket_aktif
        self.created_at = created_at

    def get_by_id(mahasiswa_id):
        return Mahasiswa.query.get(int(mahasiswa_id))

    def set_mahasiswa(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during adding Mahasiswa: {e}")
            return None

        try:
            transkip = Transkip(mahasiswa_id=self.id, semester='Semester 1', ips=0.0, created_at=datetime.utcnow(),
                                updated_at=datetime.utcnow())
            db.session.add(transkip)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during adding Transkip: {e}")
            return None

        return self
