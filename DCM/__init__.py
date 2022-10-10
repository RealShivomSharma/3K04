from flask import Flask 

#Creates flask application
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'wskldihwsdsiou9812342918371298321k' #Secures session data

    from .pages import pages
    from .auth import auth

    app.register_blueprint(pages, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    return app