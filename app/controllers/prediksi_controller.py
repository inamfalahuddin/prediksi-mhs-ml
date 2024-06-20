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
