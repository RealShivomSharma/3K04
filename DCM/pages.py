"""
Pages.py
- Contains the views that the user can go through unrelated to authentication
- At the current moment the homepage is presented to the user so that they can input programmable parameters
into the pacemaker through the DCM. 
"""
import serial
import serial.tools.list_ports
import struct
from struct import pack, unpack
import json
from time import sleep, time
from random import random
from serial.serialutil import SerialException
from serial.tools.list_ports import comports
from flask_login import login_required, current_user #Imports multiple utilities from flask_login
from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response #imports multiple utilities from flask
from .databases import * #Imports all functions from databases.py
from . import database #Imports database file
pages = Blueprint('pages', __name__) #Gives the blueprint for the page object
@pages.route('/', methods = ['GET', 'POST']) #Gives the route both POST and GET methods to send and receive data
@login_required #Ensures that user is logged in before they can access the page
def home():
    values = [time() * 1000, random() *1000]
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
    
    port_Name = ""
    portSerial = ""
    port_object = None
    for port in comports(): 
        if port.serial_number == "000000123456":
            port_Name = port.device
            portSerial = port.serial_number

    paramList = [120, 60, 5, 5, 5, 1, 250, 320, 60, 5, 2, 30, 5, 8]
    if request.method == 'POST': #If the user is posting data
        pacingMode = request.form.get('pacingModes') #Get the pacing mode from the form
        URL = request.form.get('URL', type = int)
        LRL = request.form.get('LRL', type = int)
        MSR = request.form.get('MSR', type = int)
        ATR_AMP = request.form.get('ATR_AMP', type = float)
        ATR_PW = request.form.get('ATR_PW', type = int)
        VENT_AMP = request.form.get('VENT_AMP', type = float)
        VENT_PW = request.form.get('VENT_PW', type = int)
        VRP = request.form.get('VRP', type = int)
        ARP = request.form.get('ARP', type = int)
        VENT_SENS = request.form.get('VENT_SENS', type = int)
        ATR_SENS = request.form.get('ATR_SENS', type = int)
        REACTION_TIME = request.form.get('REACTION_TIME', type = float)
        RECOVERY_TIME = request.form.get('RECOVERY_TIME', type = float)
        RESPONSE_FACTOR = request.form.get('RESPONSE_FACTOR', type = float)
        ACTIVITY_THRESHOLD = request.form['options']
        
        """
        Setting nominal inputs if user has not entered a value otherwise, checks for conflicts afterwards 
        """
        if (URL== "" or URL == None):
            URL = 120
        if (LRL== "" or LRL == None):
            LRL = 60
        if (ATR_AMP == "" or ATR_AMP == None):
            ATR_AMP = 5
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
            MSR = 60
        if (VENT_SENS == "" or VENT_SENS == None):
            VENT_SENS = 5
        if (ATR_SENS == "" or ATR_SENS == None):
            ATR_SENS = 2
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
        paramList = [URL, LRL, ATR_AMP, VENT_AMP, VENT_PW, ATR_PW, ARP, VRP, MSR, VENT_SENS, ATR_SENS, ATR_SENS, REACTION_TIME, RECOVERY_TIME, RESPONSE_FACTOR]
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
        ACT_THRES = 1.2
        match ACTIVITY_THRESHOLD:
            case "V-High":
                ACT_THRES = 2.5
            case "High":
                ACT_THRES = 2.1
            case "Med-High":
                ACT_THRES = 1.6
            case "Med":
                ACT_THRES = 1.2
            case "Med-Low":
                ACT_THRES = 0.8
            case "Low":
                ACT_THRES = 0.5
            case "V-Low":
                ACT_THRES = 0.2
        mode = struct.pack('B', pacing)
        RA_on = struct.pack('B', RA)
        URL_b = struct.pack('B', URL) 
        LRL_b = struct.pack('B', LRL)
        MSR_b = struct.pack('B', MSR)
        ATR_PW_b = struct.pack('B', ATR_PW)
        VENT_PW_b = struct.pack('B', VENT_PW)
        VENT_SENS_b = struct.pack('B', VENT_SENS)
        ATR_SENS_b = struct.pack('B', ATR_SENS)
        RESPONSE_FACTOR_b = struct.pack('B',RESPONSE_FACTOR)
        VENT_AMP_b = struct.pack('f', VENT_AMP)
        REACTION_TIME_b = struct.pack('f', REACTION_TIME)
        RECOVERY_TIME_b = struct.pack('f', RECOVERY_TIME)
        ATR_AMP_b = struct.pack('f', ATR_AMP)
        ACT_THRES_b = struct.pack('f', ACT_THRES)
        ARP_b = struct.pack('H', ARP)
        VRP_b = struct.pack('H', VRP)
        
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
        setREACTION_TIME(REACTION_TIME, pacingMode)
        setRECOVERY_TIME(RECOVERY_TIME, pacingMode)
        setRESPONSE_FACTOR(RESPONSE_FACTOR, pacingMode)
        setVENT_SENS(VENT_SENS, pacingMode)
        setATR_SENS(ATR_SENS, pacingMode)
        setACTIVITY_THRESHOLD(ACTIVITY_THRESHOLD, pacingMode)
        
        data = b'\x16'+ b'\x55' + mode + RA_on + LRL_b + URL_b + MSR_b + ATR_PW_b + VENT_PW_b + VENT_SENS_b + ATR_SENS_b + RESPONSE_FACTOR_b + VENT_AMP_b + REACTION_TIME_b + RECOVERY_TIME_b  + ATR_AMP_b + ACT_THRES_b + ARP_b + VRP_b 
        data_echo = b'\x16' + b'\x22' + mode + RA_on + LRL_b + URL_b + MSR_b + ATR_PW_b + VENT_PW_b + VENT_SENS_b + ATR_SENS_b + RESPONSE_FACTOR_b + VENT_AMP_b + REACTION_TIME_b + RECOVERY_TIME_b  + ATR_AMP_b + ACT_THRES_b + ARP_b + VRP_b 
        """if(port_object != None):
            serWrite(port_object)
        print(port_object)"""
        if (port_Name != ""):
            with serial.Serial(port = port_Name, baudrate = 115200) as ser:
                ser.write(data)
            with serial.Serial(port = port_Name, baudrate = 115200) as ser:
                ser.write(data_echo)
                
                ser.close()
        
        flash("Parameters updated succesfully") #Shows user that the parameters they have inputted successfully updated
    
    if request.method == 'GET':
        print("test")
        
        
    return render_template("home.html", user = current_user, home = 'TRUE', portName = portSerial, portStat = port_Name, paramList = paramList)