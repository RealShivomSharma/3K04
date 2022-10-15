#Contains routes for where users can navigate
from flask_login import login_required, current_user
from flask import Blueprint, render_template #Contains pages with multiple files

pages = Blueprint('pages', __name__)
@pages.route('/', methods = ['GET', 'POST'])
@login_required
def home():
    
    return render_template("home.html", user = current_user, home = 'TRUE')
