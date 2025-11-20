import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fwohfhufwuiefhwefwefwefwefwefwef'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Paystack configuration
    PAYSTACK_PUBLIC_KEY = os.environ.get('PAYSTACK_PUBLIC_KEY')
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
    
    # Investment settings
    DAILY_INTEREST_RATE = 0.5  # 0.5% per working day
    INTEREST_MATURITY_DAYS = 20  # Working days