from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager
database = SQLAlchemy()
DB_NAME = "database.db"

#Creates flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wskldihwsdsiou9812342918371298321k' #Secures session data
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    database.init_app(app) #Gives database access to flask app
    
    from .pages import pages
    from .auth import auth

    app.register_blueprint(pages, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .databases import User, Note
    
    with app.app_context():
        database.create_all()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app) 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #Looks for primary key of the user 
    return app