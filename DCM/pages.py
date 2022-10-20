#Contains routes for where users can navigate
from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .databases import *
from . import database
pages = Blueprint('pages', __name__)
@pages.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    choices = [(str(x), str(x)) for x in range(1,20)]
    selected = request.args.get('choice', '1')
    state = {'choice': selected}
    if request.method == 'POST':
        pacingMode = request.form.get('pacingModes')
        VENT_AMP = request.form.get('VENT_AMP')
        ATR_AMP = request.form.get('ATR_AMPP')
        print(VENT_AMP)
        print(ATR_AMP)
        setMode(pacingMode)

        flash("Parameters updated succesfully")

        
    
    return render_template("home.html", user = current_user, home = 'TRUE', choices = choices, state = state)
