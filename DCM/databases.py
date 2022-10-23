"""
databases.py 
- Contains all major database functions and handling of the database. Allows user to set various parameters 
in the future will contain GETTERS if necessary as well as functions to navigate the database given the current model. 
"""


from . import database #Importing database sqlAlchemy
from flask_login import UserMixin #Gives user object flask login parameters
from sqlalchemy.sql import func #Imports sql alchemy func library
from flask_wtf import FlaskForm  #Import flask forms from WTFLASK
from flask_login import current_user #Import the current_user function from flask login
from flask import flash #Import the flash function from flask (flashes error messages)

"""
Pacing class:
Contains the database entries for all of the pacing modes, it contains the user_id as a Foreign Key
This means that there is a one-to-many relationship I.E. "One user has many pacing modes and parameters associated"
Contains all programmable parameters for the pacemaker that are inputted through the DCM i  nterface
"""
class Pacing(database.Model):
    user_id = database.Column(database.Integer, database.ForeignKey('user.id')) #User id is an integer entry
    id = database.Column(database.Integer, primary_key = True) #id of the pacing mode entry is the primary key
    mode = database.Column(database.String(4), unique = True) #Every mode must have a unique entry in the database as it will be edited
    LRL = database.Column(database.Integer) #LOWER RATE LIMIT
    URL = database.Column(database.Integer) #UPPER  RATE LIMIT
    ATR_AMP = database.Column(database.Integer) #ATRIAL AMPLITUDE 
    ATR_PULSE_WIDTH = database.Column(database.Integer) #ATRIAL PULSE WIDTH LIMIT
    VENT_AMP = database.Column(database.Integer) #VENTRICULAR AMPLITUDE 
    VENT_PULSE_WIDTH = database.Column(database.Integer) #vENTRICULAR PULSE WIDTH
    VRP = database.Column(database.Integer) #
    ARP = database.Column(database.Integer) #LOWER RATE LIMIT

"""
User Class:
Contains a unique id for every user entry 
Holds and handles the storage of the user's password and username, as well as pacing data
"""
class User(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(150), unique=True) #Maximum length = 150, only unique usernames
    password = database.Column(database.String(150)) #Passowrd has a maximum string length of 150 characters
    pacing = database.relationship('Pacing') #Creates a relationship between the user and the pacing mode entries in the database

"""
countUsers function:
Returns the number of users based on a query of the number of rows in database holding User data
"""
def countUsers(database):
    return database.session.query(User).count()
"""
VARIOUS SETTER FUNCTIONS TO SET PARAMETERS IN DATABASE
"""

def setMode(mode_input):
    if (Pacing.query.filter_by(mode = mode_input).first()): #If pacing mode exists
        return #Don't change the pacing mode entry
    else: #Otherwise set the current pacing mode to the pacing mode in the form, alongside the user's id 
        pacingMode = Pacing(mode = mode_input, user_id = current_user.id) 
        database.session.add(pacingMode) #add new pacing mode to the database, corresponding to the user
        database.session.commit() #Commit the session to finalize the changes made to the database

def setLRL(database, LRL_input):
    LRL = Pacing(LRL = LRL_input, user_id = current_user.id)
    database.session.add(LRL)
    database.session.commit() 

def setURL(database, URL_input):
    URL = Pacing(LRL = URL_input, user_id = current_user.id)
    database.session.add(URL)
    database.session.commit() 

def setATR_AMP(database, ATR_AMP_input):
    ATR_AMP = Pacing(ATR_AMP = ATR_AMP_input, user_id = current_user.id)
    database.session.add(ATR_AMP)
    database.session.commit() 

def setVENT_AMP(database, VENT_AMP_input):
    VENT_AMP = Pacing(VENT_AMP = VENT_AMP_input, user_id = current_user.id)
    database.session.add(VENT_AMP)
    database.session.commit() 

def setATR_PW(database, ATR_PULSE_WIDTH_input):
    ATR_PW = Pacing(ATR_PULSE_WIDTH = ATR_PULSE_WIDTH_input, user_id = current_user.id)
    database.session.add(ATR_PW)
    database.session.commit() 

def setVENT_PW(database, VENT_PULSE_WIDTH_input):
    VENT_PW = Pacing(VENT_PULSE_WIDTH = VENT_PULSE_WIDTH_input, user_id = current_user.id)
    database.session.add(VENT_PW)
    database.session.commit() 

def setVRP(database, VRP_input):
    VRP = Pacing(VRP = VRP_input, user_id = current_user.id)
    database.session.add(VRP)
    database.session.commit() 

def setARP(database, ARP_input):
    ARP = Pacing(ARP = ARP_input, user_id = current_user.id)
    database.session.add(ARP)
    database.session.commit() 


