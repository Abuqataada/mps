from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField, BooleanField, FloatField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange
from werkzeug.security import check_password_hash

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=10, max=15)])
    service_type = SelectField('Service Interested In', choices=[
        ('', 'Select Service'),
        ('micro_fund', 'Micro Mutual Funds'),
        ('real_estate', 'Real Estate Investment'),
        ('community_finance', 'Community Finance'),
        ('pos_services', 'POS Services'),
        ('printing', 'Printing Services'),
        ('partnership', 'Partnership'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=5, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Message')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class WithdrawalForm(FlaskForm):
    amount = FloatField('Withdrawal Amount (₦)', validators=[
        DataRequired(),
        NumberRange(min=100, message='Minimum withdrawal is ₦100')
    ])
    bank_name = StringField('Bank Name', validators=[DataRequired()])
    account_number = StringField('Account Number', validators=[DataRequired(), Length(min=10, max=10)])
    account_name = StringField('Account Name', validators=[DataRequired()])
    submit = SubmitField('Request Withdrawal')

class CommunityDonationForm(FlaskForm):
    donation_type = SelectField('Donation Type', choices=[
        ('one_time', 'One-time Donation'),
        ('monthly', 'Monthly Donation')
    ], validators=[DataRequired()])
    
    frequency = SelectField('Monthly Amount (if monthly)', choices=[
        ('', 'Select monthly amount'),
        ('250', '₦250 Monthly'),
        ('500', '₦500 Monthly'), 
        ('1000', '₦1,000 Monthly')
    ])
    
    custom_amount = FloatField('Custom Amount (₦)', validators=[
        NumberRange(min=100, message='Minimum donation is ₦100')
    ])
    
    submit = SubmitField('Proceed to Donate')

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired(), Length(max=20)])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('prefer_not_to_say', 'Prefer not to say')
    ], validators=[DataRequired()])
    occupation = StringField('Occupation', validators=[DataRequired(), Length(max=100)])
    
    # Address fields
    nationality = StringField('Nationality', validators=[DataRequired(), Length(max=100)])
    state = StringField('State', validators=[DataRequired(), Length(max=100)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    street_address = StringField('Street Address', validators=[DataRequired(), Length(max=200)])
    postal_code = StringField('Postal Code', validators=[Length(max=20)])
    
    submit = SubmitField('Update Profile')

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')