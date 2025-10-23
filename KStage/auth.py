from flask import Blueprint, flash, render_template, request, url_for, redirect
from .forms import LoginForm, RegisterForm
from flask_login import login_user, login_required, logout_user
from flask_bcrypt import generate_password_hash, check_password_hash
from .models import User
from . import db 



# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)
#tester
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()

    #the validation of form is fine, HTTP request is POST
    if (register_form.validate_on_submit()==True):
            email = register_form.email.data
            #check if a user exists
            user = db.session.scalar(db.select(User).where(User.email == email))
            if user:#this returns true when user is not None
                flash('Email already exists, please try another')
                return redirect(url_for('auth.register'))
            #create a new User model object
            new_user = User(
                first_name=register_form.first_name.data.strip(),
                surname=register_form.surname.data.strip(),
                email=email,
                phone_number=(register_form.phone_number.data or '').strip(),
                street_address=(register_form.street_address.data or '').strip(),
            )
            
            new_user.set_password(register_form.password.data)
            db.session.add(new_user)
            db.session.commit()

            #Flash success for user registration 
            flash('Registration successful! Please log in with your email.', 'success')
            #commit to the database and redirect to HTML page
            return redirect(url_for('auth.login', email=new_user.email))
    #the else is called when the HTTP request calling this page is a GET
    else:
        return render_template('register.html', form=register_form, heading='Register')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        email= form.email.data.strip().lower()
        password = form.password.data

        user = db.session.scalar(db.select(User).where(User.email == email))

        # Email not registered
        if user is None:
            flash('This email is not registered. Please register an account.', 'warning') #could be a security risk to give this much info away
            return redirect(url_for('auth.register', email=email))
                
        # Incorrect password
        if not user.check_password(password):
            flash('Incorrect password. Please try again.', 'danger')
            return render_template('login.html', form=form, heading='Login')

        #All details are good/ correct    
        else: 
            login_user(user)
            flash(f'Welcome back, {user.first_name}!', 'success')
            return redirect(url_for('main.index'))
        
        # if error is None:
        #     login_user(user)
        #     return redirect(url_for('main.index'))
        # else:
        #     flash(error)

    return render_template('login.html', form=form, heading='Login')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))







#NOT WORKING :(
# #Register
# @auth_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     """Registers a new user with hashed password."""
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
    
#     form = RegisterForm()
#     if form.validate_on_submit():
#         #See/ check if email already exists 
#         existing_user = User.query.filter_by(email=form.email.data.lower()).first()
#         if existing_user:
#             flash('Email already registered. Please log in.', 'warning')
#             return redirect(url_for('auth.login'))
        
#         user = User(
#             first_name=form.first_name.data.strip(),
#             surname=form.surname.data.strip(),
#             email=form.email.data.lower().strip(),
#             phone_number=form.phone_number.data.strip(),
#             street_address=form.street_address.data.strip()
#         )
#         user.set_password(form.password.data)
#         db.session.add(user)
#         db.session.commit()

#         flash('Registration successful! You can now log in.', 'success')
#         return redirect(url_for('auth.login'))
    
#     return render_template('register.html', form=form)

# # Login 
# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     """Logs a user in aftere validating credentials."""
#     if current_user.is_authenticated:
#         return redirect(url_for('main.index'))
    
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data.lower()).first()
#         if user and user.check_password(form.password.data):
#             login_user(user)
#             flash('Login successful!', 'success')
#             next_page = request.args.get('next')
#             return redirect(next_page or url_for('main.index'))
#         else:
#             flash('Invalid email or password.', 'danger')

#     return render_template('login.html', form=form)
    


# #Logout 
# @auth_bp.route('/logout')
# @login_required
# def logout():
#     """Logs out the current user."""
#     logout_user()
#     flash('You have been logged out.', 'info')
#     return redirect(url_for('main.index'))

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
