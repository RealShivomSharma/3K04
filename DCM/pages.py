#Contains routes for where users can navigate
 
from flask import Blueprint, render_template #Contains pages with multiple files

pages = Blueprint('pages', __name__)

@pages.route('/')
def home():
    return render_template("home.html")