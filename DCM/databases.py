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
    ATR_PW = database.Column(database.Integer) #ATRIAL PULSE WIDTH LIMIT
    VENT_AMP = database.Column(database.Integer) #VENTRICULAR AMPLITUDE 
    VENT_PW = database.Column(database.Integer) #vENTRICULAR PULSE WIDTH
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

def getMode(mode_input):
    mode = Pacing.query.filter_by(mode=mode_input, user_id = current_user.id).first()
    return mode
"""
VARIOUS SETTER FUNCTIONS TO SET PARAMETERS IN DATABASE
"""

def setMode(mode_input):
    if (Pacing.query.filter_by(user_id=current_user.id, mode = mode_input).first()): #If pacing mode exists
        return #Don't change the pacing mode entry
    else: #Otherwise set the current pacing mode to the pacing mode in the form, alongside the user's id 
        pacingMode = Pacing(mode = mode_input, user_id = current_user.id) 
        database.session.add(pacingMode) #add new pacing mode to the database, corresponding to the user
        database.session.commit() #Commit the session to finalize the changes made to the database
    
def setLRL(LRL_input, mode_input):
    mode = getMode(mode_input)
    if (LRL_input == "" or LRL_input == None):
        return
    mode.input = LRL_input
    database.session.commit() 

def setURL(URL_input, mode_input):
    mode = getMode(mode_input)
    if (URL_input == "" or URL_input == None):
        return
    mode.URL = URL_input
    database.session.commit() 

def setATR_AMP(ATR_AMP_input, mode_input):
    mode = getMode(mode_input)
    if (ATR_AMP_input == "" or ATR_AMP_input == None or mode_input == "VOO" or mode_input == "VVI"):
        return
    mode.ATR_AMP = ATR_AMP_input
    database.session.commit() 

def setVENT_AMP(VENT_AMP_input, mode_input):
    
    mode = getMode(mode_input)
    if (VENT_AMP_input == "" or VENT_AMP_input == None or mode_input == "AOO" or mode_input == "AAI"):
        return
    mode.VENT_AMP = VENT_AMP_input
    database.session.commit() 
    print(mode_input)

def setATR_PW(ATR_PW_input, mode_input):
    mode = getMode(mode_input) 
    if (ATR_PW_input == "" or ATR_PW_input == None or mode_input == "VOO" or mode_input ==  "VVI"):
        return
    mode.ATR_PW = ATR_PW_input
    database.session.commit() 

def setVENT_PW(VENT_PW_input, mode_input):
    mode = getMode(mode_input) 
    if (VENT_PW_input == "" or VENT_PW_input == None or mode_input == "AOO" or mode_input == "AAI"):
        return
    mode.VENT_PW = VENT_PW_input
    database.session.commit() 


def setVRP(VRP_input, mode_input):
    mode = getMode(mode_input) 
    if (VRP_input == "" or VRP_input == None or mode_input == "AOO" or mode_input == "VOO" or mode_input == "AAI"):
        return
    mode.VRP = VRP_input
    database.session.commit()  

def setARP(ARP_input, mode_input):
    mode = getMode(mode_input) 
    if (ARP_input == "" or ARP_input == None or mode_input == "AOO" or mode_input == "VOO" or mode_input == "VVI"):
        return
    mode = getMode(mode_input)
    mode.ARP = ARP_input
    database.session.commit() 

def setPVARP(PVARP_input, mode_input):
    mode = getMode(mode_input) 
    if (PVARP_input == "" or PVARP_input == None or mode_input == "AOO" or mode_input == "VOO"):
        return
    mode = getMode(mode_input)
    mode.PVARP = PVARP_input
    database.session.commit() 

def setHysteresis(HYSTERESIS_input, mode_input):
    mode = getMode(mode_input) 
    if (HYSTERESIS_input == "" or HYSTERESIS_input == None or mode_input == "AOO" or mode_input == "VOO"):
        return
    mode = getMode(mode_input)
    mode.Hysteresis = HYSTERESIS_input
    database.session.commit() 

def setRate_Smoothing(RATE_SMOOTHING_input, mode_input):
    mode = getMode(mode_input) 
    if (RATE_SMOOTHING_input == "" or RATE_SMOOTHING_input == None or mode_input == "AOO" or mode_input == "VOO"):
        return
    mode = getMode(mode_input)

    mode.Rate_Smoothing = RATE_SMOOTHING_input
    database.session.commit()    


