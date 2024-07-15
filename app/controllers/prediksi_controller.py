import os
from joblib import load
from app.models.transkip import Transkip

model_path = os.path.join(os.path.dirname(__file__), '..', '..', 'rf_prediksi')
model_path = os.path.abspath(model_path)


def prediksi_mahasiswa(mahasiswa_id):
    model = load(model_path)

    x = Transkip.get_data_transkip(mahasiswa_id)

    prediction = model.predict(x)

    if prediction[0] == 1:
        return 'Lulus Tepat Waktu'
    else:
        return 'Tidak Lulus Tepat Waktu'


def prediksi_mahasiswa_ipk(mhs_id):
    mahasiswa = Transkip.get_transkip_by_mhs_id(mhs_id)

    data = []
    total_ips = 0
    total_sks = 0
    total_semester = 0

    for mhs in mahasiswa:
        mhs_dict = {
            'id': mhs.id,
            'mhs_id': mhs.mahasiswa_id,
            'semester': mhs.semester,
            'ips': mhs.ips,
            'sks': mhs.sks,
        }

        data.append(mhs_dict)

        total_ips += mhs.ips
        total_sks += mhs.sks
        total_semester += 1

    meta = {
        'mhs_id': mhs_id,
        'ipk': round(total_ips / total_semester, 2),  # or format(total_ips / total_semester, '.2f')
        'total_sks': total_sks,
        'total_semester': total_semester,
    }

    return {'meta': meta, 'data': data}
