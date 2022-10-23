"""
Pages.py
- Contains the views that the user can go through unrelated to authentication
- At the current moment the homepage is presented to the user so that they can input programmable parameters
into the pacemaker through the DCM. 
"""

from flask_login import login_required, current_user #Imports multiple utilities from flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for #imports multiple utilities from flask
from .databases import * #Imports all functions from databases.py
from . import database #Imports database file

pages = Blueprint('pages', __name__) #Gives the blueprint for the page object
@pages.route('/', methods = ['GET', 'POST']) #Gives the route both POST and GET methods to send and receive data
@login_required #Ensures that user is logged in before they can access the page
def home(): 
    if request.method == 'POST': #If the user is posting data
        pacingMode = request.form.get('pacingModes') #Get the pacing mode from the form
        setMode(pacingMode) #Adds the mode to the database

        flash("Parameters updated succesfully") #Shows user that the parameters they have inputted successfully updated

        
    
    return render_template("home.html", user = current_user, home = 'TRUE')
