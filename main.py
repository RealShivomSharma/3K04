"""
Contains the main running sequence to create the flask app for the DCM interface
"""
from DCM import create_app

app = create_app() #Creates instance of the flask app

if (__name__ == '__main__'): #Only run web server if file is run directly
    app.run(debug = True) #Runs web server and application
    #debug = True any changes in code will rerun the website
