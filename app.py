from app import create_app  # باید 'app' را وارد کنید چون فایل __init__.py در پوشه 'app' است

app = create_app()  # ایجاد اپلیکیشن با استفاده از تابع create_app

if __name__ == '__main__':
    app.run(debug=True)  # اجرا کردن اپلیکیشن
