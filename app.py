from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Investment, Withdrawal, CommunityDonation, SiteVisitor, Transaction
from config import Config
from datetime import datetime, date
import requests
import json
from forms import ContactForm, LoginForm
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    # If user is already logged in, redirect to dashboard
    if current_user.is_authenticated:
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
            print(f"User {user.email} logged in successfully")
            
            # Redirect to next page if it exists, otherwise to dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
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
        amount = float(request.form.get('amount'))
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
            flash('Payment initialization failed')
    
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

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:  # You'll need to add is_admin field to User model
        flash('Access denied')
        return redirect(url_for('dashboard'))
    
    # Statistics
    total_visitors = SiteVisitor.query.count()
    total_users = User.query.count()
    total_investments = Investment.query.filter_by(is_active=True).count()
    total_investment_amount = db.session.query(db.func.sum(Investment.amount)).scalar() or 0
    total_donations = CommunityDonation.query.filter_by(is_active=True).count()
    
    # Visitor statistics
    today_visitors = SiteVisitor.query.filter_by(visit_date=date.today()).count()
    recent_visitors = SiteVisitor.query.order_by(SiteVisitor.visit_time.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_visitors=total_visitors,
                         total_users=total_users,
                         total_investments=total_investments,
                         total_investment_amount=total_investment_amount,
                         today_visitors=today_visitors,
                         recent_visitors=recent_visitors,
                         total_donations=total_donations)

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


with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)