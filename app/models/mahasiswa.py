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

    def set_mahasiswa_from_excel(self):
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

    def create_mahasiswa_from_excel(self, data):
        try:
            mahasiswa_list = []
            for index, row in data.iterrows():
                mahasiswa = Mahasiswa(
                    npm=row['NPM'],
                    nama=row['Nama'],
                    prodi=row['Program Studi'],
                    tahun_masuk=row['Tahun Masuk'],
                    ket_aktif=row['Status Mahasiswa'],
                    ket_lulus=row['Status Lulus'],
                )
                db.session.add(mahasiswa)
                mahasiswa_list.append(mahasiswa)

            db.session.commit()

            for mahasiswa in mahasiswa_list:
                row = data.loc[data['NPM'] == mahasiswa.npm].iloc[0]
                for semester in range(1, 8):
                    ips_column = f'IPS{semester}'
                    sks_column = f'SKS{semester}'
                    semester_number = f'Semester {semester}'
                    ips_value = row[ips_column]
                    sks_value = row[sks_column]

                    transkip = Transkip(
                        mahasiswa_id=mahasiswa.id,
                        semester=f'Semester {semester_number}',
                        ips=ips_value,
                        sks=sks_value,
                    )
                    db.session.add(transkip)

            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return False
