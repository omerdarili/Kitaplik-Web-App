from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

# flask'a veritabanimizin nerede oldugunu ve nasil baglanacagini anlat
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgRe.1@localhost/kitaplik_db'
# bu ayar sqlalchemyin gereksiz uyarilarini engeller
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy nesnesini olusturma; db nesnesi, veritabani ile iletisimimizi saglayacak
db = SQLAlchemy(app)

# VERI MODELLERINI (TABLO PLANLARI) TANIMLAMA

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # kullanicinin kitaplari ile iliskilendirme, 
    # backref ile kullaniciya ait kitaplara kolayca ulasilabilir
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(80), nullable=False)

    # yabanci anahtar: bu kolon, kitabin hangi kullaniciya ait oldugunu gosterir
    # users.id, users tablosundaki id kolonunna baglanti kurar
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Book {self.title}'


# bu komutlar, yukarida taninlanan python siniflarini okur ve postgresql veritabanina karsilik
# gelen tablolari olusturur
with app.app_context():
    print("Veritabani tablolari olusturuluyor...")
    db.create_all()
    print("Tablolar basariyla olusturuldu.")       