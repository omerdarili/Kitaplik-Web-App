import os #isletim sistemiyle konusmak icin
from dotenv import load_dotenv # .env dosyasini okur

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# .env dosyasindaki degiskenleri yukler
load_dotenv()

# uygulama ve veritabani kurulumu
app = Flask(__name__)

# os.getenv('DEGISKEN_ADI', 'varsayilan deger') -> ortamda degiskeni bulamazsa varsayilani kullanir
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key-for-development')

# flask'a veritabanimizin nerede oldugunu ve nasil baglanacagini anlat
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

# bu ayar sqlalchemyin gereksiz uyarilarini engeller
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# sqlalchemy nesnesini olusturma; db nesnesi, veritabani ile iletisimimizi saglayacak
db = SQLAlchemy(app)

# flask-migrate kurulumu yapildi, migrate nesnesini uygulamamiza ve veritabani nesnemize bagliyoruz
migrate = Migrate(app, db)

# GUVENLIK SISTEMİ 

login_manager = LoginManager() #guvenlik sefi olusturuyoruz
login_manager.init_app(app) # sefe hangi uygulamayi koruyacagini soyluyoruz
login_manager.login_view = 'login' # eger giris yapilmamissa ve giris yapması gereken bir
                                   # sayfaya girmeye calirsirsa onu yonlendirecegimiz sayfanın fonk adini
                                   # belirtiyoruz, (login e yonlendirecek)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# VERI MODELLERINI (TABLO PLANLARI) TANIMLAMA

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    books = db.relationship('Book', backref='user', lazy=True)


    def set_password(self, password):
        # aldigi duz metni sifreyi hashler ve password_hash alanina kaydeder
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # disaridan aldigi düz metin sifreyi, veritabanindaki hash ile karsilastirir
        return check_password_hash(self.password_hash, password)    

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

@login_manager.user_loader
def load_user(user_id):
    # flask-login in verdigi user_id yi kullanarak veritabanindan ilgili kullaniciyi buluyoruz
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def home():
    # veritabanından tüm kitapları cekiyoruz
    book_list = Book.query.filter_by(user_id=current_user.id).all()
    # bu listeyi 'index.html' dosyasina 'books' adıyla gonderiyoruz
    return render_template('index.html', books=book_list)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Başarıyla giriş yaptınız!')
            return redirect(url_for('home'))
        else:
            flash('Hatalı kullanıcı adı veya şifre.', 'danger')
        flash('Hatalı kullanıcı adı veya şifre!')
    return render_template('login.html')    

@app.route('/logout') 
@login_required     
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Bu kullanıcı adı zaten alınmış.', 'warning')
            return redirect(url_for('register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu! Lütfen giriş yapın.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')
             
@app.route('/add', methods=['GET', 'POST'])
def add_book():
    # eger form gonderildi yani metot POST ise
    if request.method == 'POST':
        # formdan gelen title ve auther verilerini alıyoruz
        title = request.form['title']
        author = request.form['author']
         
        new_book = Book(title=title, author=author, user_id=current_user.id)

        # yeni kitap nesnesini veritabanı oturumuna ekliyoruz
        db.session.add(new_book)
        # degisiklikleri veritabanına kalıcı olarak isliyoruz
        db.session.commit()
        flash(f"'{new_book.title}' başarıyla eklendi!", 'success')

        # islem bittikten sonra kullanıcıyı ana sayfaya yönlendiriyoruz
        return redirect(url_for('home'))
    
    # sadece ziyaret edildiyse (yani metot GET ise)
    # kullanıcıya yeni kiap ekleme formunu gosteriyoruz
    return render_template('add_book.html')

@app.route('/delete/<int:book_id>')
@login_required
def delete_book(book_id):
    # silinecek kitabi id sine gore veritabanından buluyoruz
    # .get_or_400() metoduo id de kitap yoksa 404 hatası verir
    book_to_delete = Book.query.get_or_404(book_id)
    if book_to_delete.user.id != current_user.id:
        return "Bu işlemi yapmaya yetkiniz yok!", 403

    # kitabi veritabanindan siliyoruz
    db.session.delete(book_to_delete)
    # degisikilkleri kalici hale getiriyoruz
    db.session.commit()
    flash(f"'{title}' başarıyla silindi.", 'info') 

    # kullanıcıyı ana sayfaya yonlendirme
    return redirect(url_for('home'))

@app.route('/update/<int:book_id>', methods=['GET', 'POST'])
def update_book(book_id):
    # güncellenecek kitabı veritabanindan buluyoruz, get ve post için gerekli
    book_to_update = Book.query.get_or_404(book_id)
    if book_to_update.user.id != current_user.id:
        return "Bu işlemi yapma yetkiniz yok!", 403
    
    # eger istek post ise, yani kullanici formu doldurup guncelle dediyse
    if request.method == 'POST':

        # buldugumuz kitabin özelligini güncelliyourz
        # ORM -> sql yazmiyoruz
        book_to_update.title = request.form['title']
        book_to_update.author = request.form['author']

        db.session.commit()
        flash(f"'{book_to_update.title}' başarıyla güncellendi!", 'success')

        return redirect(url_for('home'))
    return render_template('update_book.html', book=book_to_update)
    

if __name__ == '__main__':
    app.run(debug=True)

    