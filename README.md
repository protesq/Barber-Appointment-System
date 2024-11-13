
# Barber Appointment System | Berber Randevu Sistemi

Bu proje, kullanıcıların berber randevusu almalarını, mevcut hizmetleri görüntülemelerini ve randevuları yönetmelerini sağlayan Flask tabanlı bir web uygulamasıdır. Uygulama, farklı kullanıcı rolleri (Müşteri, Berber, Admin) için özel yetkiler sunmaktadır.

This project is a Flask-based web application that allows users to book barber appointments, view available services, and manage appointments. The app includes different user roles (Customer, Barber, Admin) with specific privileges.

- **Önemli** instance adında bir dosya oluşturup db.sqlite 'ı içine atınız.

## Özellikler | Features

- **Kullanıcı Kaydı ve Doğrulama**: Şifrelenmiş parolalar ile güvenli kayıt ve giriş.
- **Rol Tabanlı Yetki Kontrolü**:
  - **Müşteri**: Randevu alabilir, görüntüleyebilir ve iptal edebilir.
  - **Berber**: Hizmetleri yönetebilir ve randevuları görebilir.
  - **Admin**: Berber ekleyebilir veya çıkarabilir, berber verilerini yönetebilir.
- **Hizmet Yönetimi**: Berberler, sundukları hizmetleri ekleyebilir, güncelleyebilir ve silebilir.
- **Randevu Yönetimi**: Belirli berberler ve hizmetler için randevu alınabilir, güncellenebilir ve iptal edilebilir.
- **Admin Paneli**: Adminlerin berberleri yönetebileceği özel bir panel.

- **User Registration & Authentication**: Secure registration and login with hashed passwords.
- **Role-Based Access Control**:
  - **Customer**: Book, view, and cancel appointments.
  - **Barber**: Manage services and view appointments.
  - **Admin**: Add or remove barbers and manage barber data.
- **Service Management**: Barbers can add, update, and delete services they offer.
- **Appointment Management**: Book, update, and cancel appointments with specific barbers and services.
- **Admin Dashboard**: A dedicated dashboard for managing barbers.

## Başlarken | Getting Started

### Gereksinimler | Prerequisites
   
- **Önemli** instance adında bir dosya oluşturup db.sqlite 'ı içine atınız.
   
- **Python 3.x** sisteminizde yüklü olmalıdır.
- **SQLite** (Varsayılan veritabanı).
- **Flask, Flask-Login, Flask-Bcrypt, ve Flask-SQLAlchemy** yüklü olmalıdır:
  
  ```bash
  pip install -r requirements.txt
  ```

- **Python 3.x** installed on your system.
- **SQLite** (default database).
- **Flask, Flask-Login, Flask-Bcrypt, and Flask-SQLAlchemy** installed. You can install dependencies using:
  
  ```bash
  pip install -r requirements.txt
  ```

### Kurulum | Installation

1. **Depoyu Klonlayın | Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd barber-appointment-system
   ```

2. **Veritabanını Oluşturun | Create Database**:
   ```bash
   python
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

3. **Uygulamayı Başlatın | Run the Application**:
   ```bash
   python app.py
   ```

4. **Uygulamaya Erişin | Access the App**:
   Tarayıcınızda `http://127.0.0.1:5000/` adresine gidin.
   
   Open your browser and navigate to `http://127.0.0.1:5000/`.

### Proje Yapısı | Project Structure

- **`app.py`**: Ana uygulama dosyası | Main application file.
- **`templates/`**: Farklı sayfalar için HTML şablonları | HTML templates for various pages.
- **`static/`**: CSS, JavaScript ve resim dosyaları | CSS, JavaScript, and image files.

## Kullanım | Usage

1. **Müşteri olarak kayıt olun | Register as a Customer**: `/register` sayfasını ziyaret edin.
2. **Giriş yapın | Log in**: `/login` sayfasına erişin.
3. **Dashboard Navigasyonu | Dashboard Navigation**:
   - **Müşteriler | Customers**: Randevu alabilir, görüntüleyebilir ve iptal edebilir.
   - **Berberler | Barbers**: Hizmet ekleyebilir, randevuları görüntüleyebilir ve fiyat güncelleyebilir.
   - **Adminler | Admins**: Berber yönetimi yapabilir ve tüm berberleri görebilir.

## Rota Özeti | Routes Overview

| Rota | Yöntem | Açıklama | Route | Method | Description |
|------|--------|----------|-------|--------|-------------|
| `/` | GET | Ana sayfa | `/` | GET | Homepage |
| `/register` | GET/POST | Kullanıcı kaydı | `/register` | GET/POST | User registration |
| `/login` | GET/POST | Kullanıcı girişi | `/login` | GET/POST | User login |
| `/admin` | GET | Admin paneli | `/admin` | GET | Admin panel |
| `/appointment` | GET/POST | Müşteri randevu yönetimi | `/appointment` | GET/POST | Customer appointment management |
| `/barber_appointments` | GET/POST | Berber randevu yönetimi | `/barber_appointments` | GET/POST | Barber appointment management |
| `/add_barber` | POST | Yeni berber ekle (Sadece Admin) | `/add_barber` | POST | Add new barber (Admin only) |
| `/delete_barber/<id>` | POST | Berber sil (Sadece Admin) | `/delete_barber/<id>` | POST | Delete barber (Admin only) |
| `/update_service_price/<id>` | POST | Berberler için hizmet fiyatı güncelleme | `/update_service_price/<id>` | POST | Update service price for barbers |
| `/logout` | GET | Kullanıcı çıkışı | `/logout` | GET | Log out user |


## Teşekkürler | Acknowledgements

- **Flask** for the web framework.
- **Flask-Login** for authentication management.
- **Flask-SQLAlchemy** for database ORM.
- **Flask-Bcrypt** for password hashing.

---

