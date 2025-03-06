from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.forms.forms import LoginForm, RegisterForm
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
import logging

auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_page'))

    form = RegisterForm()
    if form.validate_on_submit():
        if User.get_user_by_username(form.username.data):
            flash('Username already exists!', 'error')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password_hash=hashed_password, is_2fa_verified=False)
        db.session.add(new_user)
        db.session.commit()

        session['pending_user'] = new_user.username
        flash('User registered successfully! Please set up 2FA.', 'success')
        logging.info(f"New user registered: {new_user.username}")

        return redirect(url_for('auth.two_factor_setup', username=new_user.username))

    return render_template('register.html', form=form)

@auth.route('/2fa_setup/<username>', methods=['GET', 'POST'])
def two_factor_setup(username):
    if 'pending_user' not in session or session['pending_user'] != username:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('auth.login'))

    user = User.get_user_by_username(username)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.register'))

    secret = user.generate_2fa_secret()
    user.set_two_factor_secret(secret)
    db.session.commit()

    flash('Scan the QR code and click "Verify OTP".', 'success')
    logging.info(f"2FA setup completed for user: {username}")

    return render_template('2fa.html', username=username, secret=secret)

@auth.route('/verify_otp/<username>', methods=['GET', 'POST'])
def verify_otp(username):
    if 'pending_user' not in session or session['pending_user'] != username:
        flash('Unauthorized access.', 'error')
        return redirect(url_for('auth.login'))

    user = User.get_user_by_username(username)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('auth.register'))

    if request.method == 'POST':
        otp = request.form.get('otp')

        if user.validate_2fa(otp):
            user.is_2fa_verified = True
            db.session.commit()

            flash('OTP Verified! You can now log in.', 'success')
            logging.info(f"User {username} successfully verified OTP.")

            session.pop('pending_user', None)

            return redirect(url_for('auth.login'))
        else:
            flash('Invalid OTP, please try again.', 'error')
            logging.warning(f"Failed OTP verification for user: {username}")

    return render_template('verify.html', username=username)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_user_by_username(form.username.data)

        if user and check_password_hash(user.password_hash, form.password.data):
            if not user.is_2fa_verified:
                flash('You must verify your OTP before logging in.', 'error')
                return redirect(url_for('auth.verify_otp', username=user.username))

            login_user(user)
            flash('Login successful!', 'success')
            logging.info(f"User {user.username} logged in successfully.")
            return redirect(url_for('dashboard.dashboard_page'))

        flash('Invalid username or password', 'error')
        logging.warning(f"Failed login attempt for username: {form.username.data}")

    return render_template('login.html', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash('You have been logged out.', 'success')
    logging.info(f"User {username} logged out.")
    return redirect(url_for('auth.login'))