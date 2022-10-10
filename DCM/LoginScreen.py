import tkinter
import customtkinter

#Creating login Screen for DCM 
loginScreen = customtkinter.CTk()
loginScreen.title("DCM Login")
loginScreen.geometry('640x480') #Initializes beginning window size
loginScreen.configure(bg ='#333333')


#Label = library.label(parent window, text)
#Initializing and storing labels
loginLabel = tkinter.Label(loginScreen, text ="Login") 
registerLabel = tkinter.Label(loginScreen, text ="Register")
usernameLabel = tkinter.Label(loginScreen, text = 'Username')
passwordLabel = tkinter.Label(loginScreen, text = 'Password')


loginLabel.grid(row = 4, column = 4)
loginScreen.mainloop()
