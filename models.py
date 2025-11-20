from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    
    # Personal Details
    full_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    occupation = db.Column(db.String(100), nullable=False)
    
    # Identity Details
    id_type = db.Column(db.String(50), nullable=False)
    id_number = db.Column(db.String(50), nullable=False)
    issued_state = db.Column(db.String(100), nullable=False)
    issued_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    
    # Address Details
    address_type = db.Column(db.String(50), nullable=False)
    nationality = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.String(20))
    
    # Authentication - INCREASED PASSWORD HASH SIZE
    password_hash = db.Column(db.String(255), nullable=False)  # Increased from 128 to 255
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with explicit foreign_keys
    investments = db.relationship('Investment', backref='user', lazy=True, 
                                 foreign_keys='Investment.user_id')
    withdrawals = db.relationship('Withdrawal', backref='user', lazy=True, 
                                 foreign_keys='Withdrawal.user_id')
    community_donations = db.relationship('CommunityDonation', backref='user', lazy=True, 
                                        foreign_keys='CommunityDonation.user_id')
    processed_withdrawals = db.relationship('Withdrawal', backref='processor', lazy=True, 
                                          foreign_keys='Withdrawal.processed_by')
    processed_transactions = db.relationship('Transaction', backref='processor', lazy=True, 
                                           foreign_keys='Transaction.processed_by')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class Investment(db.Model):
    __tablename__ = 'investments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NGN')
    investment_type = db.Column(db.String(50), nullable=False)  # mutual_fund, real_estate
    start_date = db.Column(db.Date, nullable=False)
    last_interest_calculation = db.Column(db.Date, nullable=False)
    total_interest = db.Column(db.Float, default=0.0)
    available_for_withdrawal = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    def calculate_interest(self):
        from datetime import datetime, timedelta
        
        # Skip weekends (0=Monday, 1=Tuesday, ..., 4=Friday)
        current_date = datetime.now(timezone.utc).date()
        days_passed = (current_date - self.last_interest_calculation).days
        
        total_interest = 0
        calculation_date = self.last_interest_calculation
        
        for _ in range(days_passed):
            calculation_date += timedelta(days=1)
            # Check if it's a working day (Monday to Friday)
            if calculation_date.weekday() < 5:  # 0-4 represents Monday-Friday
                daily_interest = self.amount * (0.5 / 100)
                total_interest += daily_interest
        
        self.total_interest += total_interest
        self.last_interest_calculation = current_date
        
        # Check if interest has matured (20 working days)
        working_days_count = self.count_working_days_since_start()
        if working_days_count >= 20:
            matured_cycles = working_days_count // 20
            self.available_for_withdrawal = self.total_interest * matured_cycles
        
        return total_interest
    
    def count_working_days_since_start(self):
        from datetime import datetime, timedelta
        
        current_date = datetime.now(timezone.utc).date()
        days_passed = (current_date - self.start_date).days
        
        working_days = 0
        temp_date = self.start_date
        
        for _ in range(days_passed + 1):
            if temp_date.weekday() < 5:  # Monday to Friday
                working_days += 1
            temp_date += timedelta(days=1)
        
        return working_days


class Withdrawal(db.Model):
    __tablename__ = 'withdrawals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NGN')
    withdrawal_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    admin_notes = db.Column(db.Text)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    processed_at = db.Column(db.DateTime)


class CommunityDonation(db.Model):
    __tablename__ = 'community_donations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_type = db.Column(db.String(20))  # monthly, one_time
    frequency = db.Column(db.String(10))  # 250, 500, 1000
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    is_active = db.Column(db.Boolean, default=True)


class SiteVisitor(db.Model):
    __tablename__ = 'site_visitors'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    visit_date = db.Column(db.Date, default=date.today)
    visit_time = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    page_visited = db.Column(db.String(100))


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='NGN')
    transaction_type = db.Column(db.String(20))  # investment, withdrawal, donation
    status = db.Column(db.String(20), default='pending')
    paystack_reference = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    admin_notes = db.Column(db.Text)
    processed_by = db.Column(db.Integer, db.ForeignKey('users.id'))