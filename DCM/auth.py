#Contains login screen and authentication

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .databases import User
from werkzeug.security import generate_password_hash, check_password_hash #Password hashing to protect user data
from . import database
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in sucessfully!', category = 'success')
                login_user(user, remember = True) # Maybe change currently will remember user's login
                return redirect(url_for('pages.home'))
            else:
                flash('Incorrect password entered. Try again!', category = 'error')
        else:
            flash('Username or password does not exist', category = 'error')


    return render_template("login.html", user = current_user)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_C = request.form.get('password_C')

        user = User.query.filter_by(username = username).first()
        if user:
            flash('User already exists.', category = 'error')
        elif password != password_C:
            flash('Passwords must match', category = 'error')
        elif len(password) < 7:
            flash('Password must contain 8 characters', category = 'error')
        else:
            #add the user to the database (max of 10)
            new_user = User(username = username, password = generate_password_hash(password, method = 'sha256'))
            database.session.add(new_user)
            database.session.commit()
            flash('Account created successfully', category = 'success')
           # login_user(user, remember = True) # Maybe change currently will remember user's login
            return redirect(url_for('pages.home'))


    return render_template("register.html", user = current_user)