from flask import Blueprint, render_template, request, flash, redirect, url_for
from .model import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            flash("Logged in successfully!", category='success')
            return redirect(url_for('view.home'))
        else:
            flash("Invalid email or password", category='error')

    return render_template('login.html',user= current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        p1 = request.form.get('password1')
        p2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Email already exists", category='error')
        elif len(email) < 4:
            flash("Email must be valid", category='error')
        elif len(firstName) < 2 or len(lastName) < 2:
            flash("Name must be more than 1 character", category='error')
        elif len(p1) < 5:
            flash("Password must be at least 5 characters", category='error')
        elif p1 != p2:
            flash("Passwords do not match", category='error')
        else:
            new_user = User(
                email=email,
                firstName=firstName,
                lastName=lastName,
                password=generate_password_hash(p1, method='pbkdf2:sha256')
            )

            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)  # ✅ FIXED
            flash("Account created successfully!", category='success')
            return redirect(url_for('view.home'))

    return render_template('signup.html',user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))