#Contains login screen and authentication

from flask import Blueprint, render_template, request, flash
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
            pass
        if len(password) < 7:
            flash('Password must contain 8 characters', category = 'error')
        else:
            #add the user to the database (max of 10)
            flash('Account created successfull', category = 'success')
            pass
    return render_template("register.html")