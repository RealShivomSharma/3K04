"""
auth.py
Contains both the login and register pages as wel as the authentication features to ensure that users are correctly logged in
handling the results accordingly.
- Uses sha256 encryption for the password for each user and verifies them through the use of hashes to ensure that data is hidden
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for #importing various flask libraries
from sqlalchemy import Integer, func, select #Importing sql alchemy functionality
import sqlalchemy as database #Importing sqlalchemy database
from .databases import User, countUsers #Import functions User and count users from databases.py
from werkzeug.security import generate_password_hash, check_password_hash #Password hashing to protect user data
from . import database
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)   #creates blueprint for the page
@auth.route('/login', methods = ['GET', 'POST']) #Gives methods of GET and POST for sending and receiving data
def login(): #Login function handles posting to the form and checking if login is verified
    if request.method == 'POST': #If user is posting to the form
        username = request.form.get('username') #Get and store the username
        password = request.form.get('password') #Get and store the username
        user = User.query.filter_by(username = username).first() #Search through the database and see if user exits
        if user:
            if check_password_hash(user.password, password): #Checks the password hash to see if it matches
                flash('Logged in sucessfully!', category = 'success') #if it does flash the message that they are in
                login_user(user, remember = True) # Maybe change currently will remember user's login
                return redirect(url_for('pages.home')) #Redirects user to the home page
            else: #Otherwise possible errors of wrong password, or non-existent user
                flash('Incorrect password entered. Try again!', category = 'error') 
        else:
            flash('Username or password does not exist', category = 'error')


    return render_template("login.html", user = current_user) #Render the login screen as the current user
    
@auth.route('/logout')
@login_required
def logout(): #Logout function sends you back to login screen
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST']) #Register function with methods of GET and POST
def register():
    if request.method == 'POST': #If the user is posting to the form
        username = request.form.get('username') #Get and store username
        password = request.form.get('password') #Get and store password
        password_C = request.form.get('password_C') #Get and store the confirmed password
        
        user = User.query.filter_by(username = username).first() #Check if user exists
        if user:
            flash('User already exists.', category = 'error') #If the user already exists flash an error
        elif password != password_C: #If the passwords don't match flash an error
            flash('Passwords must match', category = 'error')
        elif len(password) < 7: #If the length of the password is less than 7 characters, flash an error
            flash('Password must contain 8 characters', category = 'error')
        elif countUsers(database) == 10: #If the number of users is already at the 10 user maximum
            flash('Max number of users reached', category = 'error' ) #Flash the max number of users being reached
        else: #Otherwise add user to the database (max of 10)
                new_user = User(username = username, password = generate_password_hash(password, method = 'sha256')) #New instance of user class
                database.session.add(new_user) #Add them to database
                database.session.commit() #Commit session to finalize changes to the database
                flash('Account created successfully', category = 'success') #Flash that user has been created succesfully 

                return redirect(url_for('pages.home')) #Redirect to the home page


    return render_template("register.html", user = current_user) #Render the register page for the current user