from flask_seeder import Seeder
import app.models


class UserSeeder(Seeder):
    def run(self):
        # Tambahkan data ke dalam tabel User
        user1 = app.models.User(username='user1', email='user1@example.com', password='password1')
        user2 = app.models.User(username='user2', email='user2@example.com', password='password2')

        self.db.session.add(user1)
        self.db.session.add(user2)
        self.db.session.commit()
