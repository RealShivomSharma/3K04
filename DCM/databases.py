from . import database #Importing database sqlAlchemy
from flask_login import UserMixin #Gives user object flask login parameters
from sqlalchemy.sql import func
class Note(database.Model):
    id = database.Column(database.Integer, primary_key =True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))


class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(150), unique=True) #Maximum length = 150, only unique usernames
    password = database.Column(database.String(150))
    notes = database.relationship('Note')
