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
        LRL = request.form.get('LRL')
        URL = request.form.get('URL')
        ATR_AMP = request.form.get('ATR_AMP')
        ATR_PW = request.form.get('ATR_PW')
        VENT_AMP = request.form.get('VENT_AMP')
        VENT_PW = request.form.get('VENT_PW')
        VRP = request.form.get('VRP')
        ARP = request.form.get('ARP')
        ACTlow = request.form.get('ACTlow')
        ACThigh = request.form.get('ACThigh')
        REACTION_TIME = request.form.get('REACTION_TIME')
        RECOVERY_TIME = request.form.get('RECOVERY_TIME')
        RESPONSE_FACTOR = request.form.get('RESPONSE_FACTOR')
        VENT_SENS = request.form.get('VENT_SENS')
        ATR_SENS = request.form.get('ATR_SENS')
        if (LRL > URL):
            flash("LRL may not exceed URL", category = 'error')
            return render_template("home.html", user = current_user, home = 'TRUE')
        if (ACTlow > ACThigh):
            flash("Low threshold may not exceed high threshold", category = 'error')
            return render_template("home.html", user = current_user, home = 'TRUE')
        
        setMode(pacingMode) #Adds the mode to the database
        setLRL(LRL, pacingMode)
        setURL(URL, pacingMode)
        setATR_AMP(ATR_AMP, pacingMode)
        setATR_PW(ATR_PW, pacingMode)
        setVENT_AMP(VENT_AMP, pacingMode)
        setVENT_PW(VENT_PW, pacingMode)
        setVRP(VRP, pacingMode)
        setARP(ARP, pacingMode)
        setACTlow(ACTlow, pacingMode)
        setACThigh(ACThigh, pacingMode)
        setREACTION_TIME(REACTION_TIME, pacingMode)
        setRECOVERY_TIME(RECOVERY_TIME, pacingMode)
        setRESPONSE_FACTOR(RESPONSE_FACTOR, pacingMode)
        setVENT_SENS(VENT_SENS, pacingMode)
        setATR_SENS(ATR_SENS, pacingMode)

        flash("Parameters updated succesfully") #Shows user that the parameters they have inputted successfully updated
    
    return render_template("home.html", user = current_user, home = 'TRUE')
