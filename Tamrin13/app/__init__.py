from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# تعریف شیء SQLAlchemy
db = SQLAlchemy()

def create_app():
    # ایجاد شیء Flask
    app = Flask(__name__)

    # تنظیمات پایگاه داده
    app.config['SECRET_KEY'] = 'your_secret_key'  # کلید مخفی برای سشن‌ها
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'  # مسیر پایگاه داده SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # غیرفعال کردن اعلان‌های تغییرات پایگاه داده

    # بارگذاری پایگاه داده در اپلیکیشن
    db.init_app(app)

    # وارد کردن و ثبت بلوپرینت‌های مورد نیاز
    from .routes import main
    app.register_blueprint(main)

    # ایجاد جداول طبق مدل‌ها
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")

    return app

