from tkinter import *
from tkinter import messagebox,simpledialog
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import mysql.connector

def login_window():
    def logfun():
        if unameE.get() == '' or upassE.get() == '':
            messagebox.showerror('Error', 'Please Enter User Name and Password......!')
        elif unameE.get() == 'Murtuza' and upassE.get() == '12345678':
            messagebox.showinfo('Success', f'Welcome {unameE.get()} to the Inventory Management System...!')
            Home.destroy()
            open_home_page()
        else:
            messagebox.showerror('Failure', 'Check your User Name and Password.....!')
    Home = Tk()
    Home.geometry('1280x720+0+0')
    Home.title("Home Page - Book Management System")
    Home.resizable(False, False)

    # Set the Background of the application
    bgimg = Image.open('/Users/murtuzaali/Downloads/DBMS Course project/360_F_612377112_vVwbnvJpfVV5s5jI1kNjsikpKlJwnk46.jpg') 
    bgimg = bgimg.resize((1280, 720))
    bgimg = ImageTk.PhotoImage(bgimg)
    bg = Label(Home, image=bgimg)
    bg.place(x=0, y=0)

    # Set a login frame on the main window of the Application
    logframe = Frame(Home, bg='white',width=300,height=2500)
    logframe.place(x=420, y=245)

    # Add content to the login frame

    # 1 - Add Logo for the login
    logimg = Image.open('/Users/murtuzaali/Downloads/DBMS Course project/WhatsApp Image 2024-09-11 at 11.32.04.jpeg')  # Update with correct path
    logimg = logimg.resize((128,128))
    logimg = ImageTk.PhotoImage(logimg)
    logo = Label(logframe, image=logimg)
    logo.grid(row=0, column=0, columnspan=2, padx=20, pady=10)  # Added padding

    # 2 - Add User Name Field
    ulogo = PhotoImage(file='/Users/murtuzaali/Downloads/Book_Management_System/Images/uname.png')  # Update with correct path
    uname = Label(logframe, image=ulogo, text='User Name: ', fg='black', bg='white', compound=LEFT)
    uname.grid(row=1, column=0, padx=10, pady=10)  # Added padding
    unameE = Entry(logframe,fg='black',bg='light grey',border=0)
    unameE.grid(row=1, column=1, padx=20, pady=10)  # Added padding

    # 3 - Add Password Field
    plogo = PhotoImage(file='/Users/murtuzaali/Downloads/DBMS Course project/pass.png')  # Update with correct path
    upass = Label(logframe, image=plogo, text='Password: ', fg='black', bg='white', compound=LEFT)
    upass.grid(row=2, column=0)  # Added padding
    upassE = Entry(logframe, show='*',fg='black',bg='light grey',border=0)
    upassE.grid(row=2, column=1, padx=80, pady=10)  # Added padding

    # 4 - Add a Login Button
    lbtn = Button(logframe, text='Login', width=15, height=2, border=0, command=logfun)
    lbtn.grid(row=3, column=0, columnspan=2, padx=70, pady=5)  # Added padding

    Home.mainloop()
