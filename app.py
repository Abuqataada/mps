from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Investment, Withdrawal, CommunityDonation, SiteVisitor, Transaction
from config import Config
from datetime import datetime, date, timezone 
import requests
import json
from forms import ContactForm, LoginForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from functools import wraps
from flask import request, jsonify
from sqlalchemy import func, desc

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Track visitors
@app.before_request
def track_visitor():
    if request.endpoint and request.endpoint != 'static':
        visitor = SiteVisitor(
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent'),
            page_visited=request.endpoint
        )
        db.session.add(visitor)
        db.session.commit()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/projects')
def projects():
    return render_template('project.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/testimonial')
def testimonial():
    return render_template('testimonial.html')

@app.route('/faqs')
def faqs():
    return render_template('faqs.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Send email notification (you'll need to configure SMTP settings)
            send_contact_email(form)
            
            flash('Your message has been sent successfully! We will get back to you soon.', 'success')
            return redirect(url_for('contact'))
            
        except Exception as e:
            flash('Sorry, there was an error sending your message. Please try again or contact us directly.', 'error')
    
    return render_template('contact.html', form=form)

def send_contact_email(form):
    # Configure your email settings
    smtp_server = "your-smtp-server.com"
    smtp_port = 587
    sender_email = "noreply@mps.com"
    sender_password = "your-email-password"
    receiver_email = "info@mps.com"
    
    # Create message
    message = MimeMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = f"New Contact Form Submission: {form.subject.data}"
    
    # Email body
    body = f"""
    New contact form submission from MPS website:
    
    Name: {form.name.data}
    Email: {form.email.data}
    Phone: {form.phone.data}
    Service: {form.service_type.data}
    Subject: {form.subject.data}
    
    Message:
    {form.message.data}
    """
    
    message.attach(MimeText(body, "plain"))
    
    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Personal Details
            full_name = request.form.get('full_name')
            date_of_birth_str = request.form.get('date_of_birth')
            email = request.form.get('email')
            mobile_number = request.form.get('mobile_number')
            gender = request.form.get('gender')
            occupation = request.form.get('occupation')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            
            # Identity Details
            id_type = request.form.get('id_type')
            id_number = request.form.get('id_number')
            issued_state = request.form.get('issued_state')
            issued_date_str = request.form.get('issued_date')
            expiry_date_str = request.form.get('expiry_date')
            
            # Address Details
            address_type = request.form.get('address_type')
            nationality = request.form.get('nationality')
            state = request.form.get('state')
            city = request.form.get('city')
            street_address = request.form.get('street_address')
            postal_code = request.form.get('postal_code')
            
            # Validate required fields
            required_fields = [
                full_name, date_of_birth_str, email, mobile_number, gender, 
                occupation, password, confirm_password, id_type, id_number,
                issued_state, issued_date_str, expiry_date_str,
                address_type, nationality, state, city, street_address
            ]
            
            if not all(required_fields):
                flash('Please fill all required fields', 'error')
                return redirect(url_for('register'))
            
            # Check if passwords match
            if password != confirm_password:
                flash('Passwords do not match', 'error')
                return redirect(url_for('register'))
            
            # Check password length
            if len(password) < 6:
                flash('Password must be at least 6 characters long', 'error')
                return redirect(url_for('register'))
            
            # Check if email already exists
            if User.query.filter_by(email=email).first():
                flash('Email already registered', 'error')
                return redirect(url_for('register'))
            
            # Check if ID number already exists
            if User.query.filter_by(id_number=id_number).first():
                flash('ID number already registered', 'error')
                return redirect(url_for('register'))
            
            # Convert date strings to date objects
            date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
            issued_date = datetime.strptime(issued_date_str, '%Y-%m-%d').date()
            expiry_date = datetime.strptime(expiry_date_str, '%Y-%m-%d').date()
            
            # Create new user
            user = User(
                # Personal Details
                full_name=full_name,
                date_of_birth=date_of_birth,
                email=email,
                mobile_number=mobile_number,
                gender=gender,
                occupation=occupation,
                
                # Identity Details
                id_type=id_type,
                id_number=id_number,
                issued_state=issued_state,
                issued_date=issued_date,
                expiry_date=expiry_date,
                
                # Address Details
                address_type=address_type,
                nationality=nationality,
                state=state,
                city=city,
                street_address=street_address,
                postal_code=postal_code
            )
            
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
            
        except ValueError as e:
            db.session.rollback()
            flash('Invalid date format. Please check your dates.', 'error')
            return redirect(url_for('register'))
        except Exception as e:
            db.session.rollback()
            flash(f'Registration failed: {str(e)}', 'error')
            return redirect(url_for('register'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to appropriate dashboard
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember.data
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            
            # Log the login
            print(f"User {user.email} logged in successfully. Admin: {user.is_admin}")
            
            # Redirect based on user role
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            if user.is_admin:
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Calculate current interests
    investments = Investment.query.filter_by(user_id=current_user.id, is_active=True).all()
    for investment in investments:
        investment.calculate_interest()
    db.session.commit()
    
    total_investment = sum(inv.amount for inv in investments)
    total_interest = sum(inv.total_interest for inv in investments)
    available_withdrawal = sum(inv.available_for_withdrawal for inv in investments)
    
    return render_template('dashboard.html', 
                         investments=investments,
                         total_investment=total_investment,
                         total_interest=total_interest,
                         available_withdrawal=available_withdrawal)

@app.route('/transactions')
@login_required
def transactions():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.created_at.desc()).all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/invest', methods=['GET', 'POST'])
@login_required
def invest():
    if request.method == 'POST':
        """amount = float(request.form.get('amount'))
        investment_type = request.form.get('investment_type')
        currency = request.form.get('currency', 'NGN')
        
        # Create investment record
        investment = Investment(
            user_id=current_user.id,
            amount=amount,
            currency=currency,
            investment_type=investment_type,
            start_date=date.today(),
            last_interest_calculation=date.today()
        )
        
        # Create transaction record
        transaction = Transaction(
            user_id=current_user.id,
            amount=amount,
            currency=currency,
            transaction_type='investment'
        )
        
        db.session.add(investment)
        db.session.add(transaction)
        db.session.commit()
        
        # Initialize Paystack payment
        paystack_data = initialize_paystack_payment(amount, email=current_user.email, reference=f"INV{transaction.id}")
        
        if paystack_data:
            return redirect(paystack_data['data']['authorization_url'])
        else:
            flash('Payment initialization failed')"""

        flash('Payment initialized. Contact support for the next step.')
        return render_template('invest.html')
    
    return render_template('invest.html')

@app.route('/withdraw', methods=['POST'])
@login_required
def withdraw():
    amount = float(request.form.get('amount'))
    currency = request.form.get('currency', 'NGN')
    
    # Check if user has available funds
    investments = Investment.query.filter_by(user_id=current_user.id, is_active=True).all()
    available_funds = sum(inv.available_for_withdrawal for inv in investments)
    
    if amount <= available_funds:
        withdrawal = Withdrawal(
            user_id=current_user.id,
            amount=amount,
            currency=currency
        )
        
        # Deduct from available funds
        # This is a simplified implementation - you might want to track which investment the withdrawal comes from
        remaining_amount = amount
        for investment in investments:
            if remaining_amount <= 0:
                break
            if investment.available_for_withdrawal > 0:
                deduct_amount = min(remaining_amount, investment.available_for_withdrawal)
                investment.available_for_withdrawal -= deduct_amount
                remaining_amount -= deduct_amount
        
        db.session.add(withdrawal)
        db.session.commit()
        
        flash('Withdrawal request submitted successfully!')
    else:
        flash('Insufficient available funds for withdrawal')
    
    return redirect(url_for('dashboard'))

@app.route('/community-donate', methods=['POST'])
@login_required
def community_donate():
    amount = float(request.form.get('amount'))
    frequency = request.form.get('frequency')
    
    donation = CommunityDonation(
        user_id=current_user.id,
        amount=amount,
        donation_type='monthly' if frequency in ['250', '500', '1000'] else 'one_time',
        frequency=frequency
    )
    
    transaction = Transaction(
        user_id=current_user.id,
        amount=amount,
        transaction_type='donation'
    )
    
    db.session.add(donation)
    db.session.add(transaction)
    db.session.commit()
    
    # Initialize Paystack payment
    paystack_data = initialize_paystack_payment(amount, email=current_user.email, reference=f"DON{transaction.id}")
    
    if paystack_data:
        return redirect(paystack_data['data']['authorization_url'])
    else:
        flash('Payment initialization failed')
    
    return redirect(url_for('dashboard'))

@app.route('/paystack/callback')
def paystack_callback():
    reference = request.args.get('reference')
    
    # Verify payment with Paystack
    verification_data = verify_paystack_payment(reference)
    
    if verification_data and verification_data['data']['status'] == 'success':
        # Update transaction status
        transaction = Transaction.query.filter_by(paystack_reference=reference).first()
        if transaction:
            transaction.status = 'completed'
            db.session.commit()
            
            flash('Payment completed successfully!')
        else:
            flash('Transaction not found')
    else:
        flash('Payment verification failed')
    
    return redirect(url_for('dashboard'))








def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Admin access required.', 'error')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# Admin Dashboard
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    # Statistics
    total_visitors = SiteVisitor.query.count()
    total_users = User.query.count()
    today_visitors = SiteVisitor.query.filter(SiteVisitor.visit_date == date.today()).count()
    total_investment_amount = db.session.query(func.sum(Investment.amount)).scalar() or 0
    total_investments = Investment.query.count()
    total_donations = CommunityDonation.query.count()
    total_withdrawals = Withdrawal.query.count()
    pending_withdrawals = Withdrawal.query.filter_by(status='pending').count()
    
    # Recent data
    recent_visitors = SiteVisitor.query.order_by(desc(SiteVisitor.visit_time)).limit(10).all()
    recent_users = User.query.order_by(desc(User.created_at)).limit(5).all()
    recent_investments = Investment.query.order_by(desc(Investment.created_at)).limit(5).all()
    
    return render_template('admin_dashboard.html',
                         total_visitors=total_visitors,
                         total_users=total_users,
                         today_visitors=today_visitors,
                         total_investment_amount=total_investment_amount,
                         total_investments=total_investments,
                         total_donations=total_donations,
                         total_withdrawals=total_withdrawals,
                         pending_withdrawals=pending_withdrawals,
                         recent_visitors=recent_visitors,
                         recent_users=recent_users,
                         recent_investments=recent_investments)

# User Management
@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    users = User.query.order_by(desc(User.created_at)).all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/user/<int:user_id>')
@login_required
@admin_required
def admin_user_detail(user_id):
    user = User.query.get_or_404(user_id)
    investments = Investment.query.filter_by(user_id=user_id).all()
    withdrawals = Withdrawal.query.filter_by(user_id=user_id).all()
    donations = CommunityDonation.query.filter_by(user_id=user_id).all()
    
    return render_template('admin_user_detail.html',
                         user=user,
                         investments=investments,
                         withdrawals=withdrawals,
                         donations=donations)

@app.route('/admin/user/toggle_active/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user_active(user_id):
    user = User.query.get_or_404(user_id)
    user.is_active = not user.is_active
    db.session.commit()
    
    action = "activated" if user.is_active else "deactivated"
    flash(f'User {user.email} has been {action}.', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/user/make_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def make_user_admin(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    db.session.commit()
    
    flash(f'User {user.email} is now an administrator.', 'success')
    return redirect(url_for('admin_users'))

# Investment Management
@app.route('/admin/investments')
@login_required
@admin_required
def admin_investments():
    investments = Investment.query.order_by(desc(Investment.created_at)).all()
    return render_template('admin_investments.html', investments=investments)

@app.route('/admin/investment/toggle_active/<int:investment_id>', methods=['POST'])
@login_required
@admin_required
def toggle_investment_active(investment_id):
    investment = Investment.query.get_or_404(investment_id)
    investment.is_active = not investment.is_active
    db.session.commit()
    
    action = "activated" if investment.is_active else "deactivated"
    flash(f'Investment #{investment.id} has been {action}.', 'success')
    return redirect(url_for('admin_investments'))

# Withdrawal Management
@app.route('/admin/withdrawals')
@login_required
@admin_required
def admin_withdrawals():
    status_filter = request.args.get('status', 'all')
    
    query = Withdrawal.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    withdrawals = query.order_by(desc(Withdrawal.withdrawal_date)).all()
    return render_template('admin_withdrawals.html', withdrawals=withdrawals, status_filter=status_filter)

@app.route('/admin/withdrawal/update_status/<int:withdrawal_id>', methods=['POST'])
@login_required
@admin_required
def update_withdrawal_status(withdrawal_id):
    withdrawal = Withdrawal.query.get_or_404(withdrawal_id)
    new_status = request.form.get('status')
    admin_notes = request.form.get('admin_notes', '')
    
    if new_status in ['pending', 'completed', 'failed']:
        withdrawal.status = new_status
        withdrawal.admin_notes = admin_notes
        withdrawal.processed_by = current_user.id
        withdrawal.processed_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'Withdrawal #{withdrawal.id} status updated to {new_status}.', 'success')
    
    return redirect(url_for('admin_withdrawals'))

# Transaction Management
@app.route('/admin/transactions')
@login_required
@admin_required
def admin_transactions():
    transactions = Transaction.query.order_by(desc(Transaction.created_at)).all()
    return render_template('admin_transactions.html', transactions=transactions)

@app.route('/admin/analytics')
@login_required
@admin_required
def admin_analytics():
    # Visitor analytics - get raw dates and convert to datetime for charting
    visitor_stats_raw = db.session.query(
        SiteVisitor.visit_date,
        func.count(SiteVisitor.id).label('visitor_count')
    ).group_by(SiteVisitor.visit_date).order_by(SiteVisitor.visit_date.desc()).limit(30).all()
    
    # Convert to proper format for charts
    visitor_stats = []
    for stat in visitor_stats_raw:
        visitor_stats.append({
            'visit_date': stat.visit_date,
            'visitor_count': stat.visitor_count
        })
    
    # User registration stats
    user_stats_raw = db.session.query(
        func.date(User.created_at).label('reg_date'),
        func.count(User.id).label('user_count')
    ).group_by(func.date(User.created_at)).order_by(desc('reg_date')).limit(30).all()
    
    user_stats = []
    for stat in user_stats_raw:
        user_stats.append({
            'reg_date': stat.reg_date,
            'user_count': stat.user_count
        })
    
    # Investment stats
    investment_stats_raw = db.session.query(
        func.date(Investment.created_at).label('inv_date'),
        func.count(Investment.id).label('investment_count'),
        func.sum(Investment.amount).label('total_amount')
    ).group_by(func.date(Investment.created_at)).order_by(desc('inv_date')).limit(30).all()
    
    investment_stats = []
    for stat in investment_stats_raw:
        investment_stats.append({
            'inv_date': stat.inv_date,
            'investment_count': stat.investment_count,
            'total_amount': float(stat.total_amount or 0)
        })
    
    return render_template('admin_analytics.html',
                         visitor_stats=visitor_stats,
                         user_stats=user_stats,
                         investment_stats=investment_stats)

# System Settings
@app.route('/admin/settings')
@login_required
@admin_required
def admin_settings():
    return render_template('admin_settings.html')

# API for charts
@app.route('/admin/api/visitor_stats')
@login_required
@admin_required
def api_visitor_stats():
    stats = db.session.query(
        SiteVisitor.visit_date,
        func.count(SiteVisitor.id).label('count')
    ).group_by(SiteVisitor.visit_date).order_by(SiteVisitor.visit_date).limit(30).all()
    
    data = {
        'dates': [stat.visit_date.strftime('%Y-%m-%d') for stat in stats],
        'counts': [stat.count for stat in stats]
    }
    
    return jsonify(data)











# Utility functions
def initialize_paystack_payment(amount, email, reference):
    url = "https://api.paystack.co/transaction/initialize"
    headers = {
        "Authorization": f"Bearer {app.config['PAYSTACK_SECRET_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "amount": int(amount * 100),  # Paystack expects amount in kobo
        "reference": reference,
        "callback_url": url_for('paystack_callback', _external=True)
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def verify_paystack_payment(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {app.config['PAYSTACK_SECRET_KEY']}"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

# Background task to calculate daily interest (should be run as a cron job)
def calculate_daily_interest():
    with app.app_context():
        investments = Investment.query.filter_by(is_active=True).all()
        for investment in investments:
            investment.calculate_interest()
        db.session.commit()

def create_admin():
    """Create an admin user"""    
    # Check if admin already exists
    existing_admin = User.query.filter_by(is_admin=True).first()
    if existing_admin:
        print(f"Admin already exists!")
        return
    
    # Create admin user
    admin = User(
        email='admin@mps.com',
        full_name='MPS Admin',
        date_of_birth=date(1990, 1, 1),  # Default DOB
        mobile_number="000-000-0000",    # Default phone
        gender="prefer_not_to_say",      # Default gender
        occupation="Administrator",      # Default occupation
        id_type="Passport",              # Default ID type
        id_number="ADMIN001",            # Default ID number
        issued_state="Federal",          # Default state
        issued_date=date.today(),        # Current date
        expiry_date=date(2030, 1, 1),    # Future date
        address_type="Residential",      # Default address type
        nationality="National",          # Default nationality
        state="Federal",                 # Default state
        city="Capital",                  # Default city
        street_address="Admin Address",  # Default address
        postal_code="00000",             # Default postal code
        is_admin=True                    # This is the important part!
    )
    admin.set_password('admin123')
    
    db.session.add(admin)
    db.session.commit()
    print(f"Admin user created successfully!")

# Run the migration
with app.app_context():
    db.create_all()
    create_admin()
        

if __name__ == '__main__':
    app.run(debug=True)