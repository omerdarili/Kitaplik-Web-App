from flask import Flask, render_template, request, redirect, url_for
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

# FLASK ROUTELARI (URL YONETIMI) #

@app.route('/')
def home():
    # veritabanından tüm kitapları cekiyoruz
    book_list = Book.query.all()
    # bu listeyi 'index.html' dosyasina 'books' adıyla gonderiyoruz
    return render_template('index.html', books=book_list)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    # eger form gonderildi yani metot POST ise
    if request.method == 'POST':
        # formdan gelen title ve auther verilerini alıyoruz
        title = request.form['title']
        author = request.form['author']
         
        new_book = Book(title=title, author=author, user_id=1)

        # yeni kitap nesnesini veritabanı oturumuna ekliyoruz
        db.sessions.add(new_book)
        # degisiklikleri veritabanına kalıcı olarak isliyoruz
        db.session.commit()

        # islem bittikten sonra kullanıcıyı ana sayfaya yönlendiriyoruz
        return redirect(url_for('home'))
    
    # sadece ziyaret edildiyse (yani metot GET ise)
    # kullanıcıya yeni kiap ekleme formunu gosteriyoruz
    return render_template('add_book.html')

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    # silinecek kitabi id sine gore veritabanından buluyoruz
    # .get_or_400() metoduo id de kitap yoksa 404 hatası verir
    book_to_delete = Book.query.get_or_404(book_id)

    # kitabi veritabanindan siliyoruz
    db.session.delete(book_to_delete)
    # degisikilkleri kalici hale getiriyoruz
    db.session.commit()

    # kullanıcıyı ana sayfaya yonlendirme
    return redirect(url_for('home'))

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    # güncellenecek kitabı veritabanindan buluyoruz, get ve post için gerekli
    book_to_update = Book.query.get_or_404(book_id)

    # eger istek post ise, yani kullanici formu doldurup guncelle dediyse
    if request.method == 'POST':
        # formdan gelen yeni bilgileri aliyoruz
        new_title = request.form['title']
        new_author = request.form['author']

        # buldugumuz kitabin özelligini güncelliyourz
        # ORM -> sql yazmiyoruz
        book_to_update.title = new_title
        book_to_update.author = new_author

        db.session.commit()

        return redirect(url_for('home'))
    

if __name__ == '__main__':
    app.run(debug=True)

    