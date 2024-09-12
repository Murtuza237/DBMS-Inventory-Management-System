from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from turtle import bgcolor
from PIL import Image, ImageTk
from tkinter import filedialog
import csv
import mysql.connector  
import subprocess

# Create Login Function for checking credentials
def logfun():
    if unameE.get() == '' or upassE.get() == '':
        messagebox.showerror('Error', 'Please Enter User Name and Password......!')
    elif unameE.get() == 'Murtuza' and upassE.get() == '12345678':
        messagebox.showinfo('Success', f'Welcome {unameE.get()} to the Inventory Management System...!')
        Home.destroy()  # Close the login window
        main_app()  # Open the inventory management system window
    else:
        messagebox.showerror('Failure', 'Check your User Name and Password.....!')

# Create GUI container for the Home Page of the Application
Home = Tk()
Home.geometry('1280x720+0+0')
Home.title("Home Page - Book Management System")
Home.resizable(False, False)

# Set the Background of the application
bgimg = Image.open('/Users/murtuzaali/Downloads/360_F_612377112_vVwbnvJpfVV5s5jI1kNjsikpKlJwnk46.jpg') 
bgimg = bgimg.resize((1280, 720))
bgimg = ImageTk.PhotoImage(bgimg)
bg = Label(Home, image=bgimg)
bg.place(x=0, y=0)

# Set a login frame on the main window of the Application
logframe = Frame(Home, bg='white',width=300,height=2500)
logframe.place(x=420, y=245)


# Add content to the login frame

# 1 - Add Logo for the login
logimg = Image.open('/Users/murtuzaali/Downloads/WhatsApp Image 2024-09-11 at 11.32.04.jpeg')  # Update with correct path
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
plogo = PhotoImage(file='/Users/murtuzaali/Downloads/Book_Management_System/Images/pass.png')  # Update with correct path
upass = Label(logframe, image=plogo, text='Password: ', fg='black', bg='white', compound=LEFT)
upass.grid(row=2, column=0)  # Added padding
upassE = Entry(logframe, show='*',fg='black',bg='light grey',border=0)
upassE.grid(row=2, column=1, padx=80, pady=10)  # Added padding

# 4 - Add a Login Button
lbtn = Button(logframe, text='Login', width=15, height=2, border=0, command=logfun)
lbtn.grid(row=3, column=0, columnspan=2, padx=70, pady=5)  # Added padding

# Main application setup
def main_app():
    global root
    root = Tk()
    root.geometry('1280x720')
    root.title('Inventory Management System')

    # Buttons for various functions
    frame = Frame(root)
    frame.pack(side=LEFT, anchor='nw', padx=10, pady=10)

    Button(frame, text='Connect to Database', command=connect_db).pack(side=TOP,fill=X, pady=5)
    Button(frame, text='Add Item', command=add_item).pack(side=TOP,fill=X, pady=5)
    Button(frame, text='Search Item', command=search_item).pack(side=TOP,fill=X, pady=5)
    Button(frame, text='Delete Item', command=delete_item).pack(side=TOP,fill=X, pady=5)
    Button(frame, text='Update Item', command=update_item).pack(side=TOP,fill=X, pady=5)


    # Treeview for displaying inventory
    global inventory
    inventory = ttk.Treeview(root, columns=('ID', 'Name', 'Description', 'UnitPrice', 'Quantity', 'ReorderLevel'), show='headings')
    inventory.heading('ID', text='ProductID')
    inventory.heading('Name', text='ProductName')
    inventory.heading('Description', text='Description')
    inventory.heading('UnitPrice', text='UnitPrice')
    inventory.heading('Quantity', text='QuantityInStock')
    inventory.heading('ReorderLevel', text='ReorderLevel')
    inventory.pack(side=RIGHT, fill='both', expand=True)
    

    root.mainloop()

# Function to connect to the database
def connect_db():
    try:
        global conn
        conn = mysql.connector.connect(
            host='localhost',
            user='Murtuza',
            password='12345678',  # Update with your MySQL password
            database='InventoryManagementSystem',  # Update with the correct database name
        )
        global cur
        cur = conn.cursor()
        messagebox.showinfo('Database Connection', 'Successfully connected to the inventory database!')
        show_items()
    except Exception as e:
        messagebox.showerror('Database Error', f'Error connecting to the database: {e}')

# Function to show all items in the Treeview
def show_items():
    for row in inventory.get_children():
        inventory.delete(row)

    try:
        cur.execute("SELECT * FROM product")  # Ensure you're selecting from the correct table
        rows = cur.fetchall()

        for idx, row in enumerate(rows, 1):
            inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
    except Exception as e:
        messagebox.showerror('Database Error', f'Error retrieving inventory: {e}')

# Function to add an item to the inventory
# Function to add an item to the inventory
def add_item():
    def save_item():
        product_name = nameE.get()
        description = descE.get()
        unit_price = priceE.get()
        quantity = quantityE.get()
        reorder_level = reorderE.get()

        if product_name == '' or description == '' or unit_price == '' or quantity == '' or reorder_level == '':
            messagebox.showerror('Input Error', 'Please fill out all fields!')
        else:
            try:
                cur.execute("INSERT INTO product (ProductName, Description, UnitPrice, QuantityInStock, ReorderLevel) VALUES (%s, %s, %s, %s, %s)",
                            (product_name, description, float(unit_price), int(quantity), int(reorder_level)))
                conn.commit()
                messagebox.showinfo('Success', 'Item added successfully!')
                addwin.destroy()
                show_items()
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding item: {e}')

    addwin = Toplevel()
    addwin.geometry('300x450')
    addwin.resizable(False, False)
    addwin.title('Add Item')

    Label(addwin, text='Product Name').pack(pady=5)
    nameE = Entry(addwin)
    nameE.pack(pady=5)

    Label(addwin, text='Description').pack(pady=5)
    descE = Entry(addwin)
    descE.pack(pady=5)

    Label(addwin, text='Unit Price').pack(pady=5)
    priceE = Entry(addwin)
    priceE.pack(pady=5)

    Label(addwin, text='Quantity In Stock').pack(pady=5)
    quantityE = Entry(addwin)
    quantityE.pack(pady=5)

    Label(addwin, text='Reorder Level').pack(pady=5)
    reorderE = Entry(addwin)
    reorderE.pack(pady=5)

    Button(addwin, text='Save Item', command=save_item).pack(pady=20)


# Function to show all items in the Treeview
def show_items():
    for row in inventory.get_children():
        inventory.delete(row)

    try:
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()

        for idx, row in enumerate(rows, 1):
            inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
    except Exception as e:
        messagebox.showerror('Database Error', f'Error retrieving inventory: {e}')

# Function to search for inventory items
def search_item():
    def perform_search():
        search_name = nameE.get()
        search_desc = descE.get()
        search_quantity_min = quantity_minE.get()
        search_quantity_max = quantity_maxE.get()

        query = "SELECT * FROM product WHERE 1=1"
        params = []

        if search_name:
            query += " AND ProductName LIKE %s"
            params.append(f"%{search_name}%")
        if search_desc:
            query += " AND Description LIKE %s"
            params.append(f"%{search_desc}%")
        if search_quantity_min:
            query += " AND QuantityInStock >= %s"
            params.append(int(search_quantity_min))
        if search_quantity_max:
            query += " AND QuantityInStock <= %s"
            params.append(int(search_quantity_max))

        try:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            inventory.delete(*inventory.get_children())
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4], row[5]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error searching inventory: {e}')

    search_win = Toplevel()
    search_win.geometry('400x350')
    search_win.resizable(False, False)
    search_win.title('Search Item')

    Label(search_win, text='Product Name').pack(pady=5)
    nameE = Entry(search_win)
    nameE.pack(pady=5)

    Label(search_win, text='Description').pack(pady=5)
    descE = Entry(search_win)
    descE.pack(pady=5)

    Label(search_win, text='Quantity Min').pack(pady=5)
    quantity_minE = Entry(search_win)
    quantity_minE.pack(pady=5)

    Label(search_win, text='Quantity Max').pack(pady=5)
    quantity_maxE = Entry(search_win)
    quantity_maxE.pack(pady=5)

    Button(search_win, text='Search', command=perform_search).pack(pady=20)

# Function to delete an inventory item from the database
def delete_item():
    def perform_delete():
        product_id = product_idE.get()

        if product_id == '':
            messagebox.showerror('Input Error', 'Please enter a Product ID!')
        else:
            try:
                cur.execute("SELECT * FROM product WHERE ProductID = %s", (product_id,))
                result = cur.fetchone()

                if result:
                    confirm = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete the item with ID {product_id}?')
                    if confirm:
                        cur.execute("DELETE FROM product WHERE ProductID = %s", (product_id,))
                        conn.commit()
                        messagebox.showinfo('Success', 'Item deleted successfully!')
                        delete_win.destroy()
                        show_items()
                    else:
                        delete_win.destroy()
                else:
                    messagebox.showerror('Error', f'No item found with ID {product_id}')
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting item: {e}')

    delete_win = Toplevel()
    delete_win.geometry('300x150')
    delete_win.resizable(False, False)
    delete_win.title('Delete Item')

    Label(delete_win, text='Enter Product ID').pack(pady=10)
    product_idE = Entry(delete_win)
    product_idE.pack(pady=5)

    Button(delete_win, text='Delete Item', command=perform_delete).pack(pady=20)

# Function to update an inventory item in the database
def update_item():
    def fetch_item():
        product_id = product_idE.get()
        if product_id == '':
            messagebox.showerror('Input Error', 'Please enter the Product ID!')
        else:
            try:
                cur.execute("SELECT * FROM product WHERE ProductID = %s", (product_id,))
                row = cur.fetchone()
                if row:
                    nameE.delete(0, END)
                    nameE.insert(0, row[1])
                    descE.delete(0, END)
                    descE.insert(0, row[2])
                    priceE.delete(0, END)
                    priceE.insert(0, row[3])
                    quantityE.delete(0, END)
                    quantityE.insert(0, row[4])
                    reorderE.delete(0, END)
                    reorderE.insert(0, row[5])
                else:
                    messagebox.showerror('Not Found', 'No item found with that ID!')
            except Exception as e:
                messagebox.showerror('Database Error', f'Error fetching item: {e}')

    def save_update():
        product_id = product_idE.get()
        product_name = nameE.get()
        description = descE.get()
        unit_price = priceE.get()
        quantity = quantityE.get()
        reorder_level = reorderE.get()

        if product_name == '' or description == '' or unit_price == '' or quantity == '' or reorder_level == '':
            messagebox.showerror('Input Error', 'Please fill out all fields!')
        else:
            try:
                cur.execute("UPDATE product SET ProductName = %s, Description = %s, UnitPrice = %s, QuantityInStock = %s, ReorderLevel = %s WHERE ProductID = %s",
                            (product_name, description, float(unit_price), int(quantity), int(reorder_level), int(product_id)))
                conn.commit()
                messagebox.showinfo('Success', 'Item updated successfully!')
                update_win.destroy()
                show_items()
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating item: {e}')

    update_win = Toplevel()
    update_win.geometry('300x550')
    update_win.resizable(False, False)
    update_win.title('Update Item')

    Label(update_win, text='Enter Product ID').pack(pady=5)
    product_idE = Entry(update_win)
    product_idE.pack(pady=5)

    Button(update_win, text='Fetch Item', command=fetch_item).pack(pady=5)

    Label(update_win, text='Product Name').pack(pady=5)
    nameE = Entry(update_win)
    nameE.pack(pady=5)

    Label(update_win, text='Description').pack(pady=5)
    descE = Entry(update_win)
    descE.pack(pady=5)

    Label(update_win, text='Unit Price').pack(pady=5)
    priceE = Entry(update_win)
    priceE.pack(pady=5)

    Label(update_win, text='Quantity In Stock').pack(pady=5)
    quantityE = Entry(update_win)
    quantityE.pack(pady=5)

    Label(update_win, text='Reorder Level').pack(pady=5)
    reorderE = Entry(update_win)
    reorderE.pack(pady=5)

    Button(update_win, text='Save Updates', command=save_update).pack(pady=20)

Home.mainloop()
