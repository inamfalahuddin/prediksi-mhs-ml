from datetime import datetime

from flask import jsonify

from app.extensions import db
from sqlalchemy.sql import text


class Transkip(db.Model):
    __tablename__ = 'transkip'
    id = db.Column(db.Integer, primary_key=True)
    mahasiswa_id = db.Column(db.Integer, db.ForeignKey('mahasiswa.id'), nullable=False)
    semester = db.Column(db.String(50), nullable=False)
    ips = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

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
        return f"Mahasiswa('{self.npm}', '{self.nama}', '{self.prodi}')"

    def get_transkip():
        result = db.session.execute(text("""
              SELECT 
                  m.id, 
                  m.npm, 
                  m.nama, 
                  m.prodi, 
                  COALESCE(GROUP_CONCAT(t.ips ORDER BY t.semester SEPARATOR ', '), '0') as ips
              FROM 
                  mahasiswa m
              LEFT JOIN 
                  transkip t 
              ON 
                  m.id = t.mahasiswa_id
              GROUP BY 
                  m.id, m.npm, m.nama, m.prodi;
          """))

        transkip_list = []
        for row in result:
            transkip_list.append({
                'id': row.id,
                'npm': row.npm,
                'nama': row.nama,
                'prodi': row.prodi,
                'ips': row.ips
            })

        return jsonify(transkip_list)
