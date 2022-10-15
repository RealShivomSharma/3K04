from . import database #Importing database sqlAlchemy
from flask_login import UserMixin #Gives user object flask login parameters
from sqlalchemy.sql import func
from flask_wtf import FlaskForm 
from flask_login import current_user


class Note(database.Model):
    id = database.Column(database.Integer, primary_key =True)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
"""
Pacing class:
Contains the database entries for all of the pacing modes, it contains the user_id as a Foreign Key
This means that there is a one-to-many relationship I.E. "One user has many pacing modes and parameters associated"
Contains all programmable parameters for the pacemaker that are inputted through the DCM i  nterface
"""
class Pacing(database.Model):
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'))
    id = database.Column(database.Integer, primary_key = True)
    mode = database.Column(database.String(4), unique = True)
    LRL = database.Column(database.Integer)
    URL = database.Column(database.Integer)
    ATR_AMP = database.Column(database.Integer)
    ATR_PULSE_WIDTH = database.Column(database.Integer)
    VENT_AMP = database.Column(database.Integer)
    VENT_PULSE_WIDTH = database.Column(database.Integer)
    VRP = database.Column(database.Integer)
    ARP = database.Column(database.Integer)

"""
User Class:
Contains a unique id for every user entry 
Holds and handles the storage of the user's password and username, as well as pacing data
"""
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(150), unique=True) #Maximum length = 150, only unique usernames
    password = database.Column(database.String(150))
    notes = database.relationship('Note')
    pacing = database.relationship('Pacing')

"""
countUsers function:
Returns the number of users based on a query of the number of rows in database holding User data
"""
def countUsers(database):
    return database.session.query(User).count()
"""
VARIOUS SETTER FUNCTIONS TO SET PARAMETERS IN DATABASE
"""

def setMode(database, mode_input):
    Pacing(mode = mode_input, user_id = current_user.id)
    database.session.commit() 

def setLRL(database, LRL_input):
    Pacing(LRL = LRL_input, user_id = current_user.id)
    database.session.commit() 

def setURL(database, URL_input):
    Pacing(LRL = URL_input, user_id = current_user.id)
    database.session.commit() 

def setATR_AMP(database, ATR_AMP_input):
    Pacing(ATR_AMP = ATR_AMP_input, user_id = current_user.id)
    database.session.commit() 

def setVENT_AMP(database, VENT_AMP_input):
    Pacing(VENT_AMP = VENT_AMP_input, user_id = current_user.id)
    database.session.commit() 

def setATR_PW(database, ATR_PULSE_WIDTH_input):
    Pacing(ATR_PULSE_WIDTH = ATR_PULSE_WIDTH_input, user_id = current_user.id)
    database.session.commit() 

def setVENT_PW(database, VENT_PULSE_WIDTH_input):
    Pacing(VENT_PULSE_WIDTH = VENT_PULSE_WIDTH_input, user_id = current_user.id)
    database.session.commit() 

def setVRP(database, VRP_input):
    Pacing(VRP = VRP_input, user_id = current_user.id)
    database.session.commit() 

def setARP(database, ARP_input):
    Pacing(ARP = ARP_input, user_id = current_user.id)
    database.session.commit() 


