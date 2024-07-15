from datetime import datetime

from app.extensions import db
from app.models.mahasiswa import Mahasiswa


class Laporan(db.Model):
    __tablename__ = 'laporan'
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    hasil_prediksi = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, mahasiswa_id, hasil_prediksi, created_at=None, updated_at=None):
        self.mahasiswa_id = mahasiswa_id
        self.hasil_prediksi = hasil_prediksi
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def __repr__(self):
        return f"Mahasiswa('{self.id}', '{self.mahasiswa_id}', '{self.hasil_prediksi}')"

    def set_laporan(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during adding Laporan: {e}")

        return self
    
    def insert_laporan(self):
        existing_record = db.session.query(Laporan).filter_by(mahasiswa_id=self.mahasiswa_id).first()

        if existing_record is None:
            db.session.add(self)
            db.session.commit()
     
    
    @staticmethod
    def get_data_laporan():
        laporan_data = (
            db.session.query(Laporan, Mahasiswa)
            .join(Mahasiswa)
            .all()
        )

        result = []
        for laporan, mahasiswa in laporan_data:
            result.append({
                'laporan_id': laporan.id,
                'mahasiswa_id': mahasiswa.id,  # Assuming you want mahasiswa's id
                'npm': mahasiswa.npm,
                'nama': mahasiswa.nama,
                'prodi': mahasiswa.prodi,
                'tahun_masuk': mahasiswa.tahun_masuk,
                'status': mahasiswa.ket_aktif,
                'prediksi': laporan.hasil_prediksi,
                'created_at': laporan.created_at,
                'updated_at': laporan.updated_at,
            })
        
        return result
