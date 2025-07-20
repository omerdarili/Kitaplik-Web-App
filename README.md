 Kitaplığım - Flask & PostgreSQL Web Uygulaması 📚

Bu proje, kullanıcıların güvenli bir şekilde kayıt olup giriş yapabildiği, kendi kişisel kitap listelerini oluşturabildiği ve bu listeler üzerinde tam kontrol (Ekleme, Güncelleme, Silme) sahibi olduğu, modern ve tam fonksiyonlu bir web uygulamasıdır.

### ✨ Uygulama Demosu

![Uygulama Demosu](![Image](https://github.com/user-attachments/assets/9dfb3372-e0e5-477a-b56a-f6bf8acec207))

---

## 🚀 Temel Özellikler

* **Güvenli Kullanıcı Yönetimi:** `Flask-Login` ile kullanıcı oturum yönetimi ve `Werkzeug` ile şifrelerin hash'lenerek güvenli bir şekilde saklandığı kayıt/giriş sistemi.
* **Kişisel Alanlar:** Her kullanıcı sadece kendi eklediği kitapları görür, düzenler ve siler. Başka kullanıcıların listelerine erişim engellenmiştir.
* **Tam CRUD Fonksiyonelliği:** Veritabanı üzerinde tam kontrol sağlayan "Create, Read, Update, Delete" operasyonları.
* **Profesyonel Veritabanı Yönetimi:** `Flask-Migrate` ile veritabanı şemasının versiyonlanarak, veri kaybı olmadan evrimleştirilmesi.
* **Güvenli Konfigürasyon:** Hassas veriler (veritabanı şifresi, gizli anahtar) `.env` dosyası ile koddan ayrılarak güvenli bir şekilde yönetilir.
* **Modern ve Mobil Uyumlu Arayüz:** `Bootstrap 5` ile oluşturulmuş, koyu tema, "cam efekti" (glassmorphism) ve animasyonlar içeren, tüm cihazlarda harika görünen şık bir tasarım.

---

## 🛠️ Kullanılan Teknolojiler

| Kategori      | Teknoloji                                       | Açıklama                                           |
|---------------|-------------------------------------------------|----------------------------------------------------|
| **Backend** | Python, Flask                                   | Uygulamanın ana mantığını ve sunucusunu yönetir.   |
| **Veritabanı**| PostgreSQL                                      | Güçlü, ilişkisel ve sektör standardı veritabanı.    |
| **ORM** | SQLAlchemy, Flask-SQLAlchemy                    | Python nesneleri ile veritabanı arasında köprü kurar.|
| **Geçişler** | Flask-Migrate                                   | Veritabanı şemasını güvenli bir şekilde günceller. |
| **Kimlik** | Flask-Login, Werkzeug.security                  | Kullanıcı oturumlarını ve şifre güvenliğini sağlar.|
| **Frontend** | HTML, Bootstrap 5, Jinja2                       | Kullanıcı arayüzünü oluşturur ve dinamik hale getirir.|
| **Güvenlik** | python-dotenv                                   | Hassas verileri koddan ayırır.                     |

---

## ⚙️ Kurulum ve Çalıştırma

Bu projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyebilirsiniz:

1.  **PostgreSQL Kurulumu:**
    Bilgisayarınızda PostgreSQL'in kurulu olduğundan ve bir veritabanı (örneğin `kitaplik_db`) oluşturduğunuzdan emin olun.

2.  **Projeyi Klonlayın:**
    ```bash
    git clone [https://github.com/omerdarili/Kitaplik-Web-App.git](https://github.com/omerdarili/Kitaplik-Web-App.git)
    cd Kitaplik-Web-App
    ```

3.  **Sanal Ortamı Oluşturun ve Aktive Edin:**
    ```bash
    # Sanal ortamı oluştur
    python -m venv venv

    # Windows için aktive etme
    .\venv\Scripts\activate

    # macOS/Linux için aktive etme
    source venv/bin/activate
    ```

4.  **Ortam Değişkenlerini Ayarlayın:**
    Proje ana dizininde `.env.example` dosyasını kopyalayıp `.env` adında yeni bir dosya oluşturun. Bu dosyanın içini kendi yerel veritabanı bilgilerinizle doldurun.
    ```
    # .env dosyası içeriği
    SECRET_KEY='tahmin-edilemez-bir-anahtar-yazin'
    DATABASE_URL='postgresql://postgres:KENDI_SIFRENIZ@localhost/kitaplik_db'
    ```

5.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

6.  **Veritabanı Tablolarını Oluşturun:**
    Flask-Migrate kullanarak veritabanı şemasını en güncel hale getirin.
    ```bash
    # (Eğer ilk kez kuruyorsanız) Migration sistemini başlatın
    # flask db init 
    
    # Veritabanını modellere göre en güncel hale getirin
    flask db upgrade
    ```

7.  **Uygulamayı Başlatın:**
    ```bash
    python app.py
    ```

8.  Tarayıcınızda `http://127.0.0.1:5000/` adresini ziyaret edin ve uygulamanın keyfini çıkarın!

---

## 📄 Lisans

Bu proje MIT Lisansı ile lisanslanmıştır.