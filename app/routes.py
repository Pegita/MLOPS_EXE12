from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Prediction
from . import db
from model.model import GoldPricePredictor

# ایجاد بلوفرینت
main = Blueprint('main', __name__)

# بارگذاری مدل یادگیری ماشین
model = GoldPricePredictor()

# صفحه اصلی
@main.route('/')
def home():
    return render_template('home.html')

# ثبت‌نام
@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # بررسی وجود کاربر
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists. Please log in.', 'danger')
            return redirect(url_for('main.login'))

        # افزودن کاربر جدید
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# ورود
@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid email or password. Please try again.', 'danger')
            return redirect(url_for('main.login'))

        # ذخیره اطلاعات کاربر در سشن
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Login successful!', 'success')
        return redirect(url_for('main.input_data'))

    return render_template('login.html')

# خروج
@main.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# دریافت ورودی برای پیش‌بینی
@main.route('/input', methods=['GET', 'POST'])
def input_data():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        open_price = float(request.form['open'])
        high_price = float(request.form['high'])
        low_price = float(request.form['low'])
        volume = float(request.form['volume'])

        # پیش‌بینی قیمت با مدل
        features = [open_price, high_price, low_price, volume]
        prediction = model.predict(features)[0]

        # ذخیره نتیجه در دیتابیس
        new_prediction = Prediction(
            user_id=session['user_id'],
            input_data=f"{features}",
            prediction_result=f"{prediction:.2f}"
        )
        db.session.add(new_prediction)
        db.session.commit()

        return render_template('result.html', prediction=prediction)

    return render_template('input.html')

# نمایش پروفایل کاربر
@main.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('main.login'))

    user = User.query.get(session['user_id'])
    predictions = Prediction.query.filter_by(user_id=user.id).all()

    return render_template('profile.html', user=user, predictions=predictions)
