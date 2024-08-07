from datetime import datetime
from sqlalchemy import func, Integer
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
    transkip = db.relationship('Transkip', backref='mahasiswa', cascade='all, delete-orphan', lazy=True)

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
            for semester_number in range(1, 8):
                transkip = Transkip(
                    mahasiswa_id=self.id,
                    semester=f'Semester {semester_number}',
                    ips=0.0,
                    sks=0,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(transkip)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error during adding Transkip: {e}")
            return None

        return self

    @staticmethod
    def get_data_transkip():
        subquery = db.session.query(
            Transkip.mahasiswa_id,
            Transkip.ips,
            Transkip.sks,
            Transkip.semester
        ).order_by(Transkip.semester).subquery()

        query = db.session.query(
            Mahasiswa.id,
            Mahasiswa.npm,
            Mahasiswa.nama,
            Mahasiswa.prodi,
            func.coalesce(func.group_concat(subquery.c.ips), '0').label('ips'),
            func.coalesce(func.group_concat(subquery.c.sks), '0').label('sks'),
            func.coalesce(func.group_concat(subquery.c.semester), '0').label('semester'),
            func.cast(func.sum(subquery.c.sks), Integer).label('total_sks'),
            func.round(func.avg(subquery.c.ips), 2).label('ipk')
        ).outerjoin(subquery, Mahasiswa.id == subquery.c.mahasiswa_id).group_by(Mahasiswa.id)

        result = query.all()

        data = []
        for row in result:
            data.append({
                "id": row.id,
                "npm": row.npm,
                "nama": row.nama,
                "prodi": row.prodi,
                "ips": [float(ip) for ip in row.ips.split(',')],  # Convert Decimal to float
                "sks": [int(sk) for sk in row.sks.split(',')],  # Convert Decimal to float
                "ipk": float(row.ipk) if row.ipk else 0.0,  # Convert Decimal to float
                "total_sks": int(row.total_sks) if row.total_sks else 0  # Convert Decimal to float
            })

        return data  # Return the list of dictionaries

    @staticmethod
    def get_by_name(name):
        return Mahasiswa.query.filter(Mahasiswa.nama.like('%' + name + '%')).all()

    @staticmethod
    def get_by_name_like(term):
        return (
            db.session.query(Mahasiswa.nama)
            .filter(Mahasiswa.nama.ilike(f'%{term}%'))  # Case-insensitive search
            .limit(10)  # Optional: limit the number of results
            .all()
        )