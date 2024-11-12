from sqlite3 import OperationalError
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from sqlalchemy import text
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin): #usermixin kullanıcı doğrulamasında işe yarar
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    customer_appointments = db.relationship('Appointment', foreign_keys='Appointment.customer_id', backref='customer', lazy=True)
    barber_appointments = db.relationship('Appointment', foreign_keys='Appointment.barber_id', backref='barber', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    barber_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    service_type = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Bekliyor', nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    barber_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    barber = db.relationship('User', backref='services')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Bu e-posta adresiyle kayıtlı bir kullanıcı zaten var.', 'danger')
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, role='Müşteri')
        db.session.add(user)
        db.session.commit()
        flash('Başarıyla kayıt oldunuz!', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Başarıyla giriş yaptınız!', 'success')
            if user.role == 'Admin':
                return redirect(url_for('admin_panel'))
            return redirect(url_for('dashboard'))
        else:
            flash('Giriş başarısız. Lütfen bilgilerinizi kontrol edin.', 'danger')
    return render_template('login.html')

@app.route('/add_barber', methods=['POST'])
@login_required
def add_barber():
    if current_user.role != 'Admin':
        flash('Bu sayfaya erişim izniniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    barber = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password, role='Berber')
    
    db.session.add(barber)
    db.session.commit()
    flash('Yeni berber başarıyla eklendi!', 'success')
    
    return redirect(url_for('admin_panel'))

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'Admin':
        flash('Bu sayfaya erişim izniniz yok.', 'danger')
        return redirect(url_for('dashboard'))
    barbers = User.query.filter_by(role='Berber').all()
    return render_template('admin.html', barbers=barbers)

@app.route('/delete_barber/<int:barber_id>', methods=['POST'])
@login_required
def delete_barber(barber_id):
    if current_user.role != 'Admin':
        flash('Bu işlemi gerçekleştirme yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    barber = User.query.get_or_404(barber_id)
    
    if barber.role != 'Berber':
        flash('Sadece berberleri silebilirsiniz.', 'danger')
        return redirect(url_for('admin_panel'))

    # Berbere ait randevuları sil
    Appointment.query.filter_by(barber_id=barber.id).delete()

    # Berbere ait hizmetleri sil
    Service.query.filter_by(barber_id=barber.id).delete()

    # Berberi sil
    db.session.delete(barber)
    db.session.commit()

    flash('Berber ve ilişkili tüm veriler başarıyla silindi!', 'success')
    return redirect(url_for('admin_panel'))

@app.route('/appointment', methods=['GET', 'POST'])
@login_required
def appointment():
    if current_user.role != 'Müşteri':
        flash('Bu sayfaya erişiminiz yok.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        barber_id = request.form['barber_id']
        appointment_date = datetime.strptime(request.form['appointment_date'], '%Y-%m-%dT%H:%M')
        service_type = request.form['service_type']

        appointment = Appointment(customer_id=current_user.id, barber_id=barber_id,
                                  appointment_date=appointment_date, service_type=service_type)
        db.session.add(appointment)
        db.session.commit()
        flash('Randevunuz başarıyla alındı!', 'success')
        return redirect(url_for('appointment'))

    barbers = User.query.filter_by(role='Berber').all()
    services = {barber.id: Service.query.filter_by(barber_id=barber.id).all() for barber in barbers}
    
    # Mevcut randevuları al
    appointments = Appointment.query.filter_by(customer_id=current_user.id).all()
    
    return render_template('appointment.html', barbers=barbers, services=services, appointments=appointments)
@app.route('/cancel_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def cancel_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    
    
    if appointment.customer_id != current_user.id:
        flash('Bu randevuyu iptal etmek için yetkiniz yok.', 'danger')
        return redirect(url_for('appointment'))
    
    appointment.status = 'İptal Edildi'
    db.session.commit()
    flash('Randevu başarıyla iptal edildi.', 'success')
    return redirect(url_for('appointment'))
@app.route('/update_service_price/<int:service_id>', methods=['POST'])
@login_required
def update_service_price(service_id):
    service = Service.query.get_or_404(service_id)
    if service.barber_id != current_user.id:
        flash('Bu hizmetin fiyatını güncelleme yetkiniz yok.', 'danger')
        return redirect(url_for('barber_appointments'))

    new_price = request.form['new_price']
    service.price = float(new_price)
    db.session.commit()
    flash('Hizmetin fiyatı başarıyla güncellendi!', 'success')
    return redirect(url_for('barber_appointments'))
@app.route('/barber_appointments', methods=['GET', 'POST'])
@login_required
def barber_appointments():
    if current_user.role != 'Berber':
        flash('Bu sayfaya erişiminiz yok.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Yeni hizmet ekleme işlemi
        service_name = request.form['service_name']
        price = float(request.form['price'])
        duration = int(request.form['duration'])

        new_service = Service(barber_id=current_user.id, service_name=service_name, price=price, duration=duration)
        db.session.add(new_service)
        db.session.commit()
        flash('Hizmet başarıyla eklendi!', 'success')
    
    # Randevular ve hizmetler
    appointments = Appointment.query.filter_by(barber_id=current_user.id).all()
    services = Service.query.filter_by(barber_id=current_user.id).all()
    return render_template('barber_appointments.html', appointments=appointments, services=services)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Berber':
        return redirect(url_for('barber_appointments'))
    elif current_user.role == 'Müşteri':
        return redirect(url_for('appointment'))
    elif current_user.role == 'Admin':
        return redirect(url_for('admin_panel'))
    else:
        flash("Bu sayfaya erişim izniniz yok.", "danger")
        return redirect(url_for('index'))

@app.route('/update_appointment/<int:appointment_id>', methods=['POST'])
@login_required
def update_appointment(appointment_id):
    if current_user.role != 'Berber':
        flash('Bu işlemi gerçekleştirmek için yetkiniz yok.', 'danger')
        return redirect(url_for('dashboard'))

    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.barber_id != current_user.id:
        flash('Bu randevuyu güncellemek için yetkiniz yok.', 'danger')
        return redirect(url_for('barber_appointments'))

    appointment.status = 'Tamamlandı'
    db.session.commit()
    flash('Randevu durumu güncellendi.', 'success')
    return redirect(url_for('barber_appointments'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
