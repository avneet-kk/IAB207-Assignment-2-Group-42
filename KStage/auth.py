from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_login import login_user, login_required, logout_user, current_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# Login 
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Logs a user in aftere validating credentials."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid email or password.', 'danger')

        return render_template('login.html', form=form)
    
#Register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Registers a new user with hashed password."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        #See/ check if email already exists 
        existing_user = User.query.filter_by(email=form.email.data.lower()).first()
        if existing_user:
            flash('Email already registered. Please log in.', 'warning')
            return redirect(url_for('auth.login'))
        
        user = User(
            first_name=form.first_name.data.strip(),
            surname=form.surname.data.strip(),
            email=form.email.data.lower().strip(),
            phone_number=form.phone_number.data.strip(),
            street_address=form.street_address.data.strip()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)


#Login - Not working (idk why its still here just incase)
# def login():
#     login_form = LoginForm()
#     error = None
#     if login_form.validate_on_submit():
#         user_name = login_form.user_name.data
#         password = login_form.password.data
#         user = db.session.scalar(db.select(User).where(User.name==user_name))
#         if user is None:
#             error = 'Incorrect user name'
#         elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
#             error = 'Incorrect password'
#         if error is None:
#             login_user(user)
#             nextp = request.args.get('next') # this gives the url from where the login page was accessed
#             print(nextp)
#             if next is None or not nextp.startswith('/'):
#                 return redirect(url_for('index'))
#             return redirect(nextp)
#         else:
#             flash(error)
#     return render_template('user.html', form=login_form, heading='Login')
