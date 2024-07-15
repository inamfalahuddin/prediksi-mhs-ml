from datetime import datetime

from app.extensions import db


class Transkip(db.Model):
    __tablename__ = 'transkip'
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    ips = db.Column(db.Float, nullable=False)
    sks = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, mahasiswa_id, semester, ips, sks, created_at=None, updated_at=None):
        self.mahasiswa_id = mahasiswa_id
        self.semester = semester
        self.ips = ips
        self.sks = sks
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def get_by_id(transkip_id):
        return Transkip.query.get(int(transkip_id))

    def set_transkip(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during adding Transkip: {e}")

        return self

    def __repr__(self):
        return f"Mahasiswa('{self.id}', '{self.mahasiswa_id}', '{self.semester}', '{self.ips}', '{self.sks}')"

    @staticmethod
    def get_data_transkip(mahasiswa_id):
        from sqlalchemy import func
        import numpy as np
        import pandas as pd

        transkip_data = db.session.query(
            func.group_concat(func.round(Transkip.ips, 2)).label('ips_array'),
            func.sum(Transkip.sks).label('total_sks')
        ).filter(Transkip.mahasiswa_id == mahasiswa_id).first()

        if transkip_data:
            ips_array, total_sks = transkip_data
            ips_array = [float(x) for x in ips_array.split(',')]  # split and convert to float

            ipk = np.mean(ips_array)  # calculate IPK
            ips_dict = {f'IPS{i + 1}': round(ips, 2) for i, ips in enumerate(ips_array)}  # round to 2 decimal places

            row = [round(ipk, 2)]
            for i in range(1, 7):
                row.append(ips_dict.get(f'IPS{i}', 0.0))
            row.append(int(total_sks))

            X = pd.DataFrame([row], columns=['IPK', 'IPS1', 'IPS2', 'IPS3', 'IPS4', 'IPS5', 'IPS6', 'Total Sks'])
            return X
        else:
            return None

    @staticmethod
    def get_transkip_by_mhs_id(mahasiswa_id):
        transkips = Transkip.query.filter_by(mahasiswa_id=mahasiswa_id).all()

        if transkips:
            return transkips
        else:
            return None
