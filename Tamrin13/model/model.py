import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

class GoldPricePredictor:
    def __init__(self):
        self.model = None
        # سعی می‌کنیم مدل ذخیره شده را بارگذاری کنیم اگر موجود باشد
        try:
            self.model = joblib.load('model/trained_model.pkl')
        except FileNotFoundError:
            print("Model not found, training a new one.")

    def train(self, data):
        """آموزش مدل با داده‌های جدید."""
        # ویژگی‌ها و هدف
        X = data[['Open', 'High', 'Low', 'Volume']]
        y = data['Close']
        
        # تقسیم داده‌ها
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # آموزش مدل
        self.model = RandomForestRegressor()
        self.model.fit(X_train, y_train)

        # ذخیره مدل
        joblib.dump(self.model, 'model/trained_model.pkl')
        print("Model trained and saved successfully!")

    def predict(self, features):
        """پیش‌بینی با استفاده از ویژگی‌های ورودی."""
        if self.model is None:
            raise ValueError("Model is not trained or loaded.")
        return self.model.predict([features])  # خروجی مدل یک آرایه است، بنابراین باید آن را از آرایه خارج کنیم
