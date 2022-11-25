"""
Pages.py
- Contains the views that the user can go through unrelated to authentication
- At the current moment the homepage is presented to the user so that they can input programmable parameters
into the pacemaker through the DCM. 
"""
import serial
import serial.tools.list_ports
import struct
from time import sleep 
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from flask_login import login_required, current_user #Imports multiple utilities from flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for #imports multiple utilities from flask
from .databases import * #Imports all functions from databases.py
from . import database #Imports database file


    

pages = Blueprint('pages', __name__) #Gives the blueprint for the page object
@pages.route('/', methods = ['GET', 'POST']) #Gives the route both POST and GET methods to send and receive data
@login_required #Ensures that user is logged in before they can access the page
def home(): 
    def __init__(self):
        self.ser = serial.Serial()
        self.conn = False
    
    def serialList(self):
        return comports()
    
    def serOpen(self, serPort):
        try:
            self.ser = serial.Serial(port = serPort, baudrate = 115200)
            self.conn = True
        except SerialException:
            self.conn = False
        
    def serClose(self):
        self.ser.close()
        self.conn = False 

    def serState(self):
        activePort = self.ser.port
        current = ""
        for port in comports():
            if activePort in port: 
                current = port
        return [self.conn, current]
    
        
    if request.method == 'POST': #If the user is posting data
        pacingMode = request.form.get('pacingModes') #Get the pacing mode from the form
        URL = request.form.get('URL')
        LRL = request.form.get('LRL')
        MSR = request.form.get('MSR')
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
        if (URL== "" or URL == None):
            URL = 120
        if (LRL== "" or LRL == None):
            LRL = 60
        if (ATR_AMP == "" or ATR_AMP == None):
            ATR_AMP = 5
        if (ATR_PW == "" or ATR_PW == None):
            ATR_PW = 1
        if (VENT_AMP == "" or VENT_AMP == None):
            VENT_AMP = 5 
        if (VENT_PW == "" or VENT_PW == None):
            VENT_PW = 1 
        if (ATR_PW == "" or ATR_PW == None):
            ATR_PW = 1
        if (ARP == "" or ARP == None):
            ARP = 250
        if (VRP == "" or VRP == None):
            VRP = 320
        if (MSR == "" or MSR == None):
            MSR = 120
        if (REACTION_TIME == "" or REACTION_TIME == None):
            REACTION_TIME = 30
        if (RECOVERY_TIME == "" or RECOVERY_TIME == None):
            RECOVERY_TIME = 5
        if (RESPONSE_FACTOR == "" or RESPONSE_FACTOR == None):
            RESPONSE_FACTOR = 8
        if (int(LRL) > int(URL)):
            flash("LRL may not exceed URL", category = 'error')
            return render_template("home.html", user = current_user, home = 'TRUE')
        if (int(MSR) > int(URL)):
            flash("MSR may not exceed URL", category = 'error')
            return render_template("home.html", user = current_user, home = 'TRUE')
        
        """
        if (ACTlow > ACThigh):
            flash("Low threshold may not exceed high threshold", category = 'error')
            return render_template("home.html", user = current_user, home = 'TRUE')
        """
        pacing = 1
        RA = 0
        match pacingMode:
            case "AOO":
                pacing = 1
                RA= 0 
            case "AAI":
                pacing = 2
                RA= 0
            case "VOO":
                pacing = 3
                RA= 0
            case "VVI":
                pacing = 4
                RA= 0
            case "AOOR":
                pacing = 1
                RA= 1
            case "AAIR":
                pacing = 2
                RA=1
            case "VOOR":
                pacing = 3
                RA=1
            case "VVIR":
                pacing = 4
                RA= 1
        setMode(pacingMode) #Adds the mode to the database
        setURL(URL, pacingMode)
        setLRL(LRL, pacingMode)
        setMSR(MSR, pacingMode)
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

        def serWrite(self):
            URL_b = struct.pack('B', URL) 
            LRL_b = struct.pack('B', LRL)
            MSR_b = struct.pack('B', MSR)
            mode = struct.pack('b', pacing)
            RA_on = struct.pack('B', RA)
            ATR_PW_b = struct.pack('B', ATR_PW)
            ATR_AMP_b = struct.pack('f', ATR_AMP)
            VENT_PW_b = struct.pack('B', VENT_PW)
            VENT_AMP_b = struct.pack('f', VENT_AMP)
            ARP_b = struct.pack('H', ARP)
            VRP_b = struct.pack('H', VRP)
            VENT_SENS_b = struct.pack('B', VENT_SENS)
            ATR_SENS_b = struct.pack('B', ATR_SENS)
            REACTION_TIME_b = struct.pack('d', REACTION_TIME)
            RECOVERY_TIME_b = struct.pack('d', RECOVERY_TIME)
            RESPONSE_FACTOR_b = struct.pack('B',RESPONSE_FACTOR)
            ACTlow_b = struct.pack('B', ACTlow)
            ACThigh_b = struct.pack('B', ACThigh)
            data = LRL_b + URL_b + MSR_b + ATR_AMP_b  + ATR_PW_b + VENT_AMP_b + VENT_PW_b + ARP_b + VRP_b + ATR_SENS_b + VENT_SENS_b + mode + RA_on + REACTION_TIME_b + RECOVERY_TIME_b + RESPONSE_FACTOR_b
            self.ser.write(data)
            sleep(0.25)

        flash("Parameters updated succesfully") #Shows user that the parameters they have inputted successfully updated
    
    return render_template("home.html", user = current_user, home = 'TRUE')
