from tkinter import *
from tkinter import messagebox,simpledialog
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import mysql.connector

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

def logout(home_page):
    # Closes the current window
    home_page.destroy()
    # Reopens the login window (assuming the login function is called login_window)
    Home.mainloop()

def open_home_page():
    home_page = Tk()
    home_page.geometry('1280x720')
    home_page.title('Inventory Management Home Page')


    # Create a frame for the heading, place it on top of the background
    heading_label = Label(home_page, text="INVENTORY MANAGEMENT SYSTEM", font=("Helvetica", 24,BOLD), bg="white", fg='black')
    heading_label.place(relx=0.5, rely=0.1, anchor='center')  # Place it centered horizontally at 10% height

    bg_image = Image.open("/Users/murtuzaali/Downloads/DBMS Course project/WhatsApp Image 2024-09-12 at 16.04.56.png")
    bg_image = bg_image.resize((1280, 720))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    background_label = Label(home_page, image=bg_photo)
    background_label.place(relwidth=1, relheight=1)

    frame = Frame(home_page, bg='white')
    frame.pack(side=LEFT, padx=50, pady=10)

    buttons = [
        ('Product', open_product_window),
        ('Order', open_orders_window),
        ('Supplier', open_supplier_window),
        ('Customer', lambda: messagebox.showinfo('Customer', 'Customer management coming soon!')),
        ('Order Details', lambda: messagebox.showinfo('Purchase Order', 'Purchase order details coming soon!')),
        ('Purchase Order Details', lambda: messagebox.showinfo('Purchase Order', 'Purchase order details coming soon!')),
        ('Category', open_category_window),
        ('Warehouse', lambda: messagebox.showinfo('Warehouse', 'Warehouse management coming soon!')),
        ('Log out',lambda: logout(home_page))
    ]

    for text, command in buttons:
        Button(frame, text=text, width=20, height=2, command=command, bg='blue').pack(pady=5)

    home_page.mainloop()