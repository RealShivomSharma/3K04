#Contains login screen and authentication

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .databases import User
from werkzeug.security import generate_password_hash, check_password_hash #Password hashing to protect user data
from . import database
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    data = request.form #Contains request information in the form (Username, password)
    print(data)
    return render_template("login.html", text = "Testing")
    
@auth.route('/logout')
def logout():
    return render_template("home.html")

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password_C = request.form.get('password_C')
    
        if password != password_C:
            flash('Passwords must match', category = 'error')
        elif len(password) < 7:
            flash('Password must contain 8 characters', category = 'error')
        else:
            #add the user to the database (max of 10)
            new_user = User(username = username, password = generate_password_hash(password, method = 'sha256'))
            database.session.add(new_user)
            database.session.commit()
            flash('Account created successfully', category = 'success')
            return redirect(url_for('pages.home'))


    return render_template("register.html")