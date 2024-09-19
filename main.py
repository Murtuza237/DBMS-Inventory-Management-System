from tkinter import *
from tkinter import messagebox,simpledialog
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import mysql.connector  
import tkinter as tk
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
        ('Product', open_products),
        ('Order', show_orders),
        ('Supplier', show_suppliers),
        ('Customer', open_customer),
        ('Purchase Order',open_purchase_orders),
        ('Purchase Order Details',open_purchase_order_details),
        ('Category', open_category_window),
        ('Warehouse',open_warehouse),
        ('Inventory Audit',open_inventory_audit),
        ('Log out',lambda: logout(home_page))
    ]

    for text, command in buttons:
        Button(frame, text=text, width=20, height=2, command=command).pack(pady=5)

    home_page.mainloop()
    
    
def logout(home_page):
    # Ask for confirmation before logging out
    response = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
    
    if response:  # If the user clicks 'Yes'
        # Close the current window
        home_page.destroy()
        # Reopen the login window (assuming you have a function called login_window)
        login_window()

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  
            user="Murtuza",       
            password="12345678",       
            database="inventorymanagementsystem"  
        )
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to the database: {err}")
        return None
    
def open_products():
    def add_product():
        # Add a new product to the database
        product_id = product_id_entry.get()
        product_name = product_name_entry.get()
        category_id = category_id_entry.get()
        quantity_in_stock = quantity_in_stock_entry.get()
        reorder_level = reorder_level_entry.get()
        unit_price = unit_price_entry.get()
        supplier_id = supplier_id_entry.get()

        if not (product_id and product_name and category_id and quantity_in_stock and reorder_level and unit_price and supplier_id):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Product (ProductID, ProductName, CategoryID, Quantity_In_Stock, Reorder_Level, UnitPrice, SupplierID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (product_id, product_name, category_id, quantity_in_stock, reorder_level, unit_price, supplier_id))
                conn.commit()
                messagebox.showinfo('Success', 'Product added successfully')
                show_win.destroy()
                open_products()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding product: {e}')
            finally:
                cur.close()
                conn.close()

    def update_product():
        # Update selected product in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a product to update')
            return

        product_id = product_id_entry.get()
        product_name = product_name_entry.get()
        category_id = category_id_entry.get()
        quantity_in_stock = quantity_in_stock_entry.get()
        reorder_level = reorder_level_entry.get()
        unit_price = unit_price_entry.get()
        supplier_id = supplier_id_entry.get()

        if not (product_id and product_name and category_id and quantity_in_stock and reorder_level and unit_price and supplier_id):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_product_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Product SET ProductID=%s, ProductName=%s, CategoryID=%s, Quantity_In_Stock=%s, 
                            Reorder_Level=%s, UnitPrice=%s, SupplierID=%s WHERE ProductID=%s""",
                            (product_id, product_name, category_id, quantity_in_stock, reorder_level, unit_price, supplier_id, selected_product_id))
                conn.commit()
                messagebox.showinfo('Success', 'Product updated successfully')
                show_win.destroy()
                open_products()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating product: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_product():
        # Delete selected product from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a product to delete')
            return

        selected_product_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Product WHERE ProductID=%s", (selected_product_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Product deleted successfully')
                show_win.destroy()
                open_products()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting product: {e}')
            finally:
                cur.close()
                conn.close()

        # Create the window
    show_win = tk.Toplevel()
    show_win.title("Product List")

    # Create Treeview for displaying products (placed at the top of the window)
    inventory = ttk.Treeview(show_win, columns=('ProductID', 'ProductName', 'CategoryID', 'Quantity_In_Stock', 'Reorder_Level', 'UnitPrice', 'SupplierID'), show='headings')
    inventory.heading('ProductID', text='ProductID')
    inventory.heading('ProductName', text='ProductName')
    inventory.heading('CategoryID', text='CategoryID')
    inventory.heading('Quantity_In_Stock', text='Quantity In Stock')
    inventory.heading('Reorder_Level', text='Reorder Level')
    inventory.heading('UnitPrice', text='Unit Price')
    inventory.heading('SupplierID', text='SupplierID')
    inventory.pack(side=tk.TOP, fill='both', expand=True)  # Treeview placed at the top

    # Form for product input (placed at the bottom of the window)
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.BOTTOM, fill='both', expand=True,padx=10)  # Form placed at the bottom

    tk.Label(form_frame, text="ProductID:").grid(row=0, column=0, sticky='w')
    product_id_entry = tk.Entry(form_frame)
    product_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ProductName:").grid(row=1, column=0, sticky='w')
    product_name_entry = tk.Entry(form_frame)
    product_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="CategoryID:").grid(row=2, column=0, sticky='w')
    category_id_entry = tk.Entry(form_frame)
    category_id_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Quantity In Stock:").grid(row=3, column=0, sticky='w')
    quantity_in_stock_entry = tk.Entry(form_frame)
    quantity_in_stock_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Reorder Level:").grid(row=4, column=0, sticky='w')
    reorder_level_entry = tk.Entry(form_frame)
    reorder_level_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Unit Price:").grid(row=5, column=0, sticky='w')
    unit_price_entry = tk.Entry(form_frame)
    unit_price_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="SupplierID:").grid(row=6, column=0, sticky='w')
    supplier_id_entry = tk.Entry(form_frame)
    supplier_id_entry.grid(row=6, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete (packed at the bottom of the form_frame)
    button_frame = tk.Frame(form_frame)
    button_frame.grid(row=7, column=0, columnspan=2, pady=10)

    add_button = tk.Button(button_frame, text="Add Product", command=add_product)
    add_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(button_frame, text="Update Product", command=update_product)
    update_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(button_frame, text="Delete Product", command=delete_product)
    delete_button.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

    # Populate the Treeview with product data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Product")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving products: {e}')
        finally:
            cur.close()
            conn.close()


def show_suppliers():
    def add_supplier():
        # Add a new supplier to the database
        supplier_id = supplier_id_entry.get()
        supplier_name = supplier_name_entry.get()
        contact_name = contact_name_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        postal_code = postal_code_entry.get()
        country = country_entry.get()
        phone = phone_entry.get()

        if not (supplier_id and supplier_name and contact_name and address and city and postal_code and country and phone):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Supplier (SupplierID, SupplierName, ContactName, Address, City, PostalCode, Country, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (supplier_id, supplier_name, contact_name, address, city, postal_code, country, phone))
                conn.commit()
                messagebox.showinfo('Success', 'Supplier added successfully')
                show_win.destroy()
                show_suppliers()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding supplier: {e}')
            finally:
                cur.close()
                conn.close()

    def update_supplier():
        # Update selected supplier in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a supplier to update')
            return

        supplier_id = supplier_id_entry.get()
        supplier_name = supplier_name_entry.get()
        contact_name = contact_name_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        postal_code = postal_code_entry.get()
        country = country_entry.get()
        phone = phone_entry.get()

        if not (supplier_id and supplier_name and contact_name and address and city and postal_code and country and phone):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_supplier_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Supplier SET SupplierID=%s, SupplierName=%s, ContactName=%s, Address=%s, City=%s, PostalCode=%s, Country=%s, Phone=%s WHERE SupplierID=%s""",
                            (supplier_id, supplier_name, contact_name, address, city, postal_code, country, phone, selected_supplier_id))
                conn.commit()
                messagebox.showinfo('Success', 'Supplier updated successfully')
                show_win.destroy()
                show_suppliers()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating supplier: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_supplier():
        # Delete selected supplier from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a supplier to delete')
            return

        selected_supplier_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Supplier WHERE SupplierID=%s", (selected_supplier_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Supplier deleted successfully')
                show_win.destroy()
                show_suppliers()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting supplier: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    show_win = tk.Toplevel()
    show_win.title("Supplier List")

    # Create Treeview for displaying suppliers
    inventory = ttk.Treeview(show_win, columns=('SupplierID', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone'), show='headings')
    inventory.heading('SupplierID', text='SupplierID')
    inventory.heading('SupplierName', text='SupplierName')
    inventory.heading('ContactName', text='ContactName')
    inventory.heading('Address', text='Address')
    inventory.heading('City', text='City')
    inventory.heading('PostalCode', text='PostalCode')
    inventory.heading('Country', text='Country')
    inventory.heading('Phone', text='Phone')
    inventory.pack(side=tk.TOP, fill='both', expand=True)  # Treeview at the top

    # Form for supplier input
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.BOTTOM, fill='x', padx=10)  # Form at the bottom

    tk.Label(form_frame, text="SupplierID:").grid(row=0, column=0, sticky='w')
    supplier_id_entry = tk.Entry(form_frame)
    supplier_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="SupplierName:").grid(row=1, column=0, sticky='w')
    supplier_name_entry = tk.Entry(form_frame)
    supplier_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ContactName:").grid(row=2, column=0, sticky='w')
    contact_name_entry = tk.Entry(form_frame)
    contact_name_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky='w')
    address_entry = tk.Entry(form_frame)
    address_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="City:").grid(row=4, column=0, sticky='w')
    city_entry = tk.Entry(form_frame)
    city_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="PostalCode:").grid(row=5, column=0, sticky='w')
    postal_code_entry = tk.Entry(form_frame)
    postal_code_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Country:").grid(row=6, column=0, sticky='w')
    country_entry = tk.Entry(form_frame)
    country_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Phone:").grid(row=7, column=0, sticky='w')
    phone_entry = tk.Entry(form_frame)
    phone_entry.grid(row=7, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Supplier", command=add_supplier)
    add_button.grid(row=8, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Supplier", command=update_supplier)
    update_button.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Supplier", command=delete_supplier)
    delete_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


    # Populate the Treeview with supplier data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Supplier")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving suppliers: {e}')
        finally:
            cur.close()
            conn.close()


def show_orders():
    def add_order():
        order_id = order_id_entry.get()
        customer_id = customer_id_entry.get()
        order_date = order_date_entry.get()
        total_amount = total_amount_entry.get()

        if not (order_id and customer_id and order_date and total_amount):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount) VALUES (%s, %s, %s, %s)",
                            (order_id, customer_id, order_date, total_amount))
                conn.commit()
                messagebox.showinfo('Success', 'Order added successfully')
                orders_win.destroy()
                show_orders()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding order: {e}')
            finally:
                cur.close()
                conn.close()

    def update_order():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order to update')
            return

        order_id = order_id_entry.get()
        customer_id = customer_id_entry.get()
        order_date = order_date_entry.get()
        total_amount = total_amount_entry.get()

        if not (order_id and customer_id and order_date and total_amount):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_order_id = tree.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Orders SET OrderID=%s, CustomerID=%s, OrderDate=%s, TotalAmount=%s WHERE OrderID=%s""",
                            (order_id, customer_id, order_date, total_amount, selected_order_id))
                conn.commit()
                messagebox.showinfo('Success', 'Order updated successfully')
                orders_win.destroy()
                show_orders()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating order: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_order():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order to delete')
            return

        selected_order_id = tree.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Orders WHERE OrderID=%s", (selected_order_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Order deleted successfully')
                orders_win.destroy()
                show_orders()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting order: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    orders_win = tk.Toplevel()
    orders_win.geometry('800x600')
    orders_win.title('Manage Orders')

    # Create a Frame for the Treeview
    treeview_frame = tk.Frame(orders_win)
    treeview_frame.pack(side=tk.TOP, fill='both', expand=True)

    # Create the Treeview
    tree = ttk.Treeview(treeview_frame, columns=("OrderID", "CustomerID", "OrderDate", "TotalAmount"), show='headings')
    tree.heading("OrderID", text="Order ID")
    tree.heading("CustomerID", text="Customer ID")
    tree.heading("OrderDate", text="Order Date")
    tree.heading("TotalAmount", text="Total Amount")
    tree.pack(fill='both', expand=True)

    # Form for order input
    form_frame = tk.Frame(orders_win)
    form_frame.pack(side=tk.BOTTOM, fill='x')

    tk.Label(form_frame, text="Order ID:").grid(row=0, column=0, sticky='w')
    order_id_entry = tk.Entry(form_frame)
    order_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Customer ID:").grid(row=1, column=0, sticky='w')
    customer_id_entry = tk.Entry(form_frame)
    customer_id_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Order Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='w')
    order_date_entry = tk.Entry(form_frame)
    order_date_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Total Amount:").grid(row=3, column=0, sticky='w')
    total_amount_entry = tk.Entry(form_frame)
    total_amount_entry.grid(row=3, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Order", command=add_order)
    add_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Order", command=update_order)
    update_button.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Order", command=delete_order)
    delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


    # Populate the Treeview with order data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Orders")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                tree.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving orders: {e}')
        finally:
            cur.close()
            conn.close()    

def open_category_window():
    category_win = Toplevel()
    category_win.geometry('800x600')
    category_win.title('Manage Categories')

    # Create a Frame for the Treeview
    treeview_frame = Frame(category_win)
    treeview_frame.pack(fill='both', expand=True)

    # Create the Treeview
    tree = ttk.Treeview(treeview_frame, columns=("CategoryID", "CategoryName", "Description"), show='headings')
    tree.heading("CategoryID", text="Category ID")
    tree.heading("CategoryName", text="Category Name")
    tree.heading("Description", text="Description")
    tree.pack(fill=BOTH, expand=True)

    # Function to update Treeview with the latest data from the database
    def update_treeview():
        # Clear the current contents of the treeview
        for row in tree.get_children():
            tree.delete(row)
        
        # Fetch the updated data and insert it into the treeview
        categories = fetch_data("SELECT * FROM Category")
        for category in categories:
            tree.insert("", END, values=category)

    # Initial data population
    update_treeview()

    # Buttons
    Button(category_win, text='Add Category', command=lambda: [add_category(), update_treeview()]).pack(pady=10)
    Button(category_win, text='Update Category', command=lambda: [update_category(), update_treeview()]).pack(pady=10)
    Button(category_win, text='Delete Category', command=lambda: [delete_category(), update_treeview()]).pack(pady=10)

# Helper function to fetch data from the database
def fetch_data(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def add_category():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    category_name = simpledialog.askstring("Input", "Enter category name:")
    description = simpledialog.askstring("Input", "Enter description:")
    query = "INSERT INTO Category (CategoryName, Description) VALUES (%s, %s)"
    cursor.execute(query, (category_name, description))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    messagebox.showinfo("Success", "Category added successfully!")

# Function to update a category
def update_category():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    category_id = simpledialog.askinteger("Input", "Enter category ID to update:")
    new_category_name = simpledialog.askstring("Input", "Enter new category name:")
    new_description = simpledialog.askstring("Input", "Enter new description:")
    query = "UPDATE Category SET CategoryName = %s, Description = %s WHERE CategoryID = %s"
    cursor.execute(query, (new_category_name, new_description, category_id))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    messagebox.showinfo("Success", "Category updated successfully!")

# Function to delete a category
def delete_category():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    category_id = simpledialog.askinteger("Input", "Enter category ID to delete:")
    query = "DELETE FROM Category WHERE CategoryID = %s"
    cursor.execute(query, (category_id,))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    messagebox.showinfo("Success", "Category deleted successfully!")
    
def open_purchase_orders():
    def add_order():
        # Add new order to the database
        po_id = po_id_entry.get()
        po_date = po_date_entry.get()
        supplier_id = supplier_id_entry.get()
        total_amount = total_amount_entry.get()

        if not (po_id and po_date and supplier_id and total_amount):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Purchase_Order (PurchaseOrder_ID, PurchaseDate, SupplierID, TotalAmount) VALUES (%s, %s, %s, %s)",
                            (po_id, po_date, supplier_id, total_amount))
                conn.commit()
                messagebox.showinfo('Success', 'Purchase order added successfully')
                show_win.destroy()
                open_purchase_orders()  # Refresh the list
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding purchase order: {e}')
            finally:
                cur.close()
                conn.close()

    def update_order():
        # Update selected order in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order to update')
            return

        po_id = po_id_entry.get()
        po_date = po_date_entry.get()
        supplier_id = supplier_id_entry.get()
        total_amount = total_amount_entry.get()

        if not (po_id and po_date and supplier_id and total_amount):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_order_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("UPDATE Purchase_Order SET PurchaseOrder_ID=%s, PurchaseDate=%s, SupplierID=%s, TotalAmount=%s WHERE PurchaseOrder_ID=%s",
                            (po_id, po_date, supplier_id, total_amount, selected_order_id))
                conn.commit()
                messagebox.showinfo('Success', 'Purchase order updated successfully')
                show_win.destroy()
                open_purchase_orders()  # Refresh the list
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating purchase order: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_order():
        # Delete selected order from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order to delete')
            return

        selected_order_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Purchase_Order WHERE PurchaseOrder_ID=%s", (selected_order_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Purchase order deleted successfully')
                show_win.destroy()
                open_purchase_orders()  # Refresh the list
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting purchase order: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the main window
    show_win = tk.Toplevel()
    show_win.title("Purchase Order List")

    # Create the Treeview
    inventory = ttk.Treeview(show_win, columns=('PurchaseOrder_ID', 'PurchaseDate', 'SupplierID', 'TotalAmount'), show='headings')
    inventory.heading('PurchaseOrder_ID', text='PurchaseOrder_ID')
    inventory.heading('PurchaseDate', text='PurchaseDate')
    inventory.heading('SupplierID', text='SupplierID')
    inventory.heading('TotalAmount', text='TotalAmount')
    inventory.pack(side=tk.LEFT, fill='both', expand=True)

    # Create the form for adding/updating orders
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.BOTTOM, fill='both', expand=True)

    tk.Label(form_frame, text="PurchaseOrder_ID:").grid(row=0, column=0, sticky='w')
    po_id_entry = tk.Entry(form_frame)
    po_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="PurchaseDate:").grid(row=1, column=0, sticky='w')
    po_date_entry = tk.Entry(form_frame)
    po_date_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="SupplierID:").grid(row=2, column=0, sticky='w')
    supplier_id_entry = tk.Entry(form_frame)
    supplier_id_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="TotalAmount:").grid(row=3, column=0, sticky='w')
    total_amount_entry = tk.Entry(form_frame)
    total_amount_entry.grid(row=3, column=1, padx=5, pady=5)

    add_button = tk.Button(form_frame, text="Add Order", command=add_order)
    add_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Order", command=update_order)
    update_button.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Order", command=delete_order)
    delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    # Populate the Treeview with data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Purchase_Order")
            rows = cur.fetchall()
            for row in rows:
                inventory.insert('', 'end', values=(row[0], row[1], row[2], row[3]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving purchase orders: {e}')
        finally:
            cur.close()
            conn.close()
            
def open_purchase_order_details():
    def add_order_detail():
        # Add new order detail to the database
        detail_id = detail_id_entry.get()
        order_id = order_id_entry.get()
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()
        unit_price = unit_price_entry.get()

        if not (detail_id and order_id and product_id and quantity and unit_price):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Purchase_Order_Details (PurchaseOrderDetailID, PurchaseOrder_ID, ProductID, Quantity, UnitPrice) VALUES (%s, %s, %s, %s, %s)",
                            (detail_id, order_id, product_id, quantity, unit_price))
                conn.commit()
                messagebox.showinfo('Success', 'Purchase order detail added successfully')
                show_win.destroy()
                open_purchase_order_details()  # Refresh the list
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding purchase order detail: {e}')
            finally:
                cur.close()
                conn.close()

    def update_order_detail():
        # Update selected order detail in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order detail to update')
            return

        detail_id = detail_id_entry.get()
        order_id = order_id_entry.get()
        product_id = product_id_entry.get()
        quantity = quantity_entry.get()
        unit_price = unit_price_entry.get()

        if not (detail_id and order_id and product_id and quantity and unit_price):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_detail_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("UPDATE Purchase_Order_Details SET PurchaseOrderDetailID=%s, PurchaseOrder_ID=%s, ProductID=%s, Quantity=%s, UnitPrice=%s WHERE PurchaseOrderDetailID=%s",
                            (detail_id, order_id, product_id, quantity, unit_price, selected_detail_id))
                conn.commit()
                messagebox.showinfo('Success', 'Purchase order detail updated successfully')
                show_win.destroy()
                open_purchase_order_details()  # Refresh the list
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating purchase order detail: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_order_detail():
        # Delete selected order detail from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order detail to delete')
            return

        selected_detail_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Purchase_Order_Details WHERE PurchaseOrderDetailID=%s", (selected_detail_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Purchase order detail deleted successfully')
                show_win.destroy()
                open_purchase_order_details()  # Refresh the list
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting purchase order detail: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the main window
    show_win = tk.Toplevel()
    show_win.title("Purchase Order Details List")

    # Create the Treeview
    inventory = ttk.Treeview(show_win, columns=('PurchaseOrderDetailID', 'PurchaseOrder_ID', 'ProductID', 'Quantity', 'UnitPrice'), show='headings')
    inventory.heading('PurchaseOrderDetailID', text='PurchaseOrderDetailID')
    inventory.heading('PurchaseOrder_ID', text='PurchaseOrder_ID')
    inventory.heading('ProductID', text='ProductID')
    inventory.heading('Quantity', text='Quantity')
    inventory.heading('UnitPrice', text='UnitPrice')
    inventory.pack(side=tk.LEFT, fill='both', expand=True)

    # Create the form for adding/updating order details
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.RIGHT, fill='both', expand=True)

    tk.Label(form_frame, text="PurchaseOrderDetailID:").grid(row=0, column=0, sticky='w')
    detail_id_entry = tk.Entry(form_frame)
    detail_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="PurchaseOrder_ID:").grid(row=1, column=0, sticky='w')
    order_id_entry = tk.Entry(form_frame)
    order_id_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ProductID:").grid(row=2, column=0, sticky='w')
    product_id_entry = tk.Entry(form_frame)
    product_id_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Quantity:").grid(row=3, column=0, sticky='w')
    quantity_entry = tk.Entry(form_frame)
    quantity_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="UnitPrice:").grid(row=4, column=0, sticky='w')
    unit_price_entry = tk.Entry(form_frame)
    unit_price_entry.grid(row=4, column=1, padx=5, pady=5)

    add_button = tk.Button(form_frame, text="Add Order Detail", command=add_order_detail)
    add_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Order Detail", command=update_order_detail)
    update_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Order Detail", command=delete_order_detail)
    delete_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')
    
    
    # Populate the Treeview with data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Purchase_Order_Details")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving purchase order details: {e}')
        finally:
            cur.close()
            conn.close()
            
def open_customer():
    def add_customer():
        # Add a new customer to the database
        customer_id = customer_id_entry.get()
        customer_name = customer_name_entry.get()
        contact_name = contact_name_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        postal_code = postal_code_entry.get()
        country = country_entry.get()
        phone = phone_entry.get()

        if not (customer_id and customer_name and contact_name and address and city and postal_code and country and phone):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Customer (CustomerID, CustomerName, ContactName, Address, City, PostalCode, Country, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (customer_id, customer_name, contact_name, address, city, postal_code, country, phone))
                conn.commit()
                messagebox.showinfo('Success', 'Customer added successfully')
                show_win.destroy()
                open_customer()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding customer: {e}')
            finally:
                cur.close()
                conn.close()

    def update_customer():
        # Update selected customer in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a customer to update')
            return

        customer_id = customer_id_entry.get()
        customer_name = customer_name_entry.get()
        contact_name = contact_name_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        postal_code = postal_code_entry.get()
        country = country_entry.get()
        phone = phone_entry.get()

        if not (customer_id and customer_name and contact_name and address and city and postal_code and country and phone):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_customer_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Customer SET CustomerID=%s, CustomerName=%s, ContactName=%s, Address=%s, 
                            City=%s, PostalCode=%s, Country=%s, Phone=%s WHERE CustomerID=%s""",
                            (customer_id, customer_name, contact_name, address, city, postal_code, country, phone, selected_customer_id))
                conn.commit()
                messagebox.showinfo('Success', 'Customer updated successfully')
                show_win.destroy()
                open_customer()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating customer: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_customer():
        # Delete selected customer from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a customer to delete')
            return

        selected_customer_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Customer WHERE CustomerID=%s", (selected_customer_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Customer deleted successfully')
                show_win.destroy()
                open_customer()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting customer: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    show_win = tk.Toplevel()
    show_win.title("Customer List")

    # Create Treeview for displaying customers
    inventory = ttk.Treeview(show_win, columns=('CustomerID', 'CustomerName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone'), show='headings')
    inventory.heading('CustomerID', text='CustomerID')
    inventory.heading('CustomerName', text='CustomerName')
    inventory.heading('ContactName', text='ContactName')
    inventory.heading('Address', text='Address')
    inventory.heading('City', text='City')
    inventory.heading('PostalCode', text='PostalCode')
    inventory.heading('Country', text='Country')
    inventory.heading('Phone', text='Phone')
    inventory.pack(side=tk.TOP, fill='both', expand=True)

    # Form for customer input
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.BOTTOM, fill='both',padx=10)

    tk.Label(form_frame, text="CustomerID:").grid(row=0, column=0, sticky='w')
    customer_id_entry = tk.Entry(form_frame)
    customer_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="CustomerName:").grid(row=1, column=0, sticky='w')
    customer_name_entry = tk.Entry(form_frame)
    customer_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ContactName:").grid(row=2, column=0, sticky='w')
    contact_name_entry = tk.Entry(form_frame)
    contact_name_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky='w')
    address_entry = tk.Entry(form_frame)
    address_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="City:").grid(row=4, column=0, sticky='w')
    city_entry = tk.Entry(form_frame)
    city_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="PostalCode:").grid(row=5, column=0, sticky='w')
    postal_code_entry = tk.Entry(form_frame)
    postal_code_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Country:").grid(row=6, column=0, sticky='w')
    country_entry = tk.Entry(form_frame)
    country_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Phone:").grid(row=7, column=0, sticky='w')
    phone_entry = tk.Entry(form_frame)
    phone_entry.grid(row=7, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Customer", command=add_customer)
    add_button.grid(row=8, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Customer", command=update_customer)
    update_button.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Customer", command=delete_customer)
    delete_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


    # Populate the Treeview with customer data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Customer")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving customers: {e}')
        finally:
            cur.close()
            conn.close()

            
def open_inventory_audit():
    def add_audit():
        # Add a new inventory audit to the database
        audit_id = audit_id_entry.get()
        product_id = product_id_entry.get()
        audit_date = audit_date_entry.get()
        quantity_checked = quantity_checked_entry.get()
        remarks = remarks_entry.get()

        if not (audit_id and product_id and audit_date and quantity_checked and remarks):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Inventory_Audit (AuditID, ProductID, Audit_Date, Quantity_Checked, Remarks) VALUES (%s, %s, %s, %s, %s)",
                            (audit_id, product_id, audit_date, quantity_checked, remarks))
                conn.commit()
                messagebox.showinfo('Success', 'Inventory audit added successfully')
                show_win.destroy()
                open_inventory_audit()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding audit: {e}')
            finally:
                cur.close()
                conn.close()

    def update_audit():
        # Update selected inventory audit in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an audit to update')
            return

        audit_id = audit_id_entry.get()
        product_id = product_id_entry.get()
        audit_date = audit_date_entry.get()
        quantity_checked = quantity_checked_entry.get()
        remarks = remarks_entry.get()

        if not (audit_id and product_id and audit_date and quantity_checked and remarks):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_audit_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Inventory_Audit SET AuditID=%s, ProductID=%s, Audit_Date=%s, 
                            Quantity_Checked=%s, Remarks=%s WHERE AuditID=%s""",
                            (audit_id, product_id, audit_date, quantity_checked, remarks, selected_audit_id))
                conn.commit()
                messagebox.showinfo('Success', 'Audit updated successfully')
                show_win.destroy()
                open_inventory_audit()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating audit: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_audit():
        # Delete selected inventory audit from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an audit to delete')
            return

        selected_audit_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Inventory_Audit WHERE AuditID=%s", (selected_audit_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Audit deleted successfully')
                show_win.destroy()
                open_inventory_audit()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting audit: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    show_win = tk.Toplevel()
    show_win.title("Inventory Audit List")

    # Create Treeview for displaying inventory audits
    inventory = ttk.Treeview(show_win, columns=('AuditID', 'ProductID', 'Audit_Date', 'Quantity_Checked', 'Remarks'), show='headings')
    inventory.heading('AuditID', text='AuditID')
    inventory.heading('ProductID', text='ProductID')
    inventory.heading('Audit_Date', text='Audit_Date')
    inventory.heading('Quantity_Checked', text='Quantity_Checked')
    inventory.heading('Remarks', text='Remarks')
    inventory.pack(side=tk.LEFT, fill='both', expand=True)

    # Form for audit input
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.RIGHT, fill='both', expand=True)

    tk.Label(form_frame, text="AuditID:").grid(row=0, column=0, sticky='w')
    audit_id_entry = tk.Entry(form_frame)
    audit_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ProductID:").grid(row=1, column=0, sticky='w')
    product_id_entry = tk.Entry(form_frame)
    product_id_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Audit_Date:").grid(row=2, column=0, sticky='w')
    audit_date_entry = tk.Entry(form_frame)
    audit_date_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Quantity_Checked:").grid(row=3, column=0, sticky='w')
    quantity_checked_entry = tk.Entry(form_frame)
    quantity_checked_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Remarks:").grid(row=4, column=0, sticky='w')
    remarks_entry = tk.Entry(form_frame)
    remarks_entry.grid(row=4, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Audit", command=add_audit)
    add_button.grid(row=5, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Audit", command=update_audit)
    update_button.grid(row=5, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Audit", command=delete_audit)
    delete_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

    # Populate the Treeview with inventory audit data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Inventory_Audit")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving audits: {e}')
        finally:
            cur.close()
            conn.close()

def open_warehouse():
    def add_warehouse():
        # Add a new warehouse to the database
        warehouse_id = warehouse_id_entry.get()
        warehouse_name = warehouse_name_entry.get()
        location = location_entry.get()

        if not (warehouse_id and warehouse_name and location):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Warehouse (WarehouseID, WarehouseName, Location) VALUES (%s, %s, %s)",
                            (warehouse_id, warehouse_name, location))
                conn.commit()
                messagebox.showinfo('Success', 'Warehouse added successfully')
                show_win.destroy()
                open_warehouse()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding warehouse: {e}')
            finally:
                cur.close()
                conn.close()

    def update_warehouse():
        # Update selected warehouse in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a warehouse to update')
            return

        warehouse_id = warehouse_id_entry.get()
        warehouse_name = warehouse_name_entry.get()
        location = location_entry.get()

        if not (warehouse_id and warehouse_name and location):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_warehouse_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Warehouse SET WarehouseID=%s, WarehouseName=%s, Location=%s 
                            WHERE WarehouseID=%s""",
                            (warehouse_id, warehouse_name, location, selected_warehouse_id))
                conn.commit()
                messagebox.showinfo('Success', 'Warehouse updated successfully')
                show_win.destroy()
                open_warehouse()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating warehouse: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_warehouse():
        # Delete selected warehouse from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a warehouse to delete')
            return

        selected_warehouse_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Warehouse WHERE WarehouseID=%s", (selected_warehouse_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Warehouse deleted successfully')
                show_win.destroy()
                open_warehouse()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting warehouse: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    show_win = tk.Toplevel()
    show_win.title("Warehouse List")

    # Create Treeview for displaying warehouses
    inventory = ttk.Treeview(show_win, columns=('WarehouseID', 'WarehouseName', 'Location'), show='headings')
    inventory.heading('WarehouseID', text='WarehouseID')
    inventory.heading('WarehouseName', text='WarehouseName')
    inventory.heading('Location', text='Location')
    inventory.pack(side=tk.LEFT, fill='both', expand=True)

    # Form for warehouse input
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.RIGHT, fill='both', expand=True)

    tk.Label(form_frame, text="WarehouseID:").grid(row=0, column=0)
    warehouse_id_entry = tk.Entry(form_frame)
    warehouse_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="WarehouseName:").grid(row=1, column=0)
    warehouse_name_entry = tk.Entry(form_frame)
    warehouse_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Location:").grid(row=2, column=0)
    location_entry = tk.Entry(form_frame)
    location_entry.grid(row=2, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Warehouse", command=add_warehouse)
    add_button.grid(row=3, column=0, padx=5, pady=5)

    update_button = tk.Button(form_frame, text="Update Warehouse", command=update_warehouse)
    update_button.grid(row=3, column=1, padx=5, pady=5)

    delete_button = tk.Button(form_frame, text="Delete Warehouse", command=delete_warehouse)
    delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Populate the Treeview with warehouse data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Warehouse")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving warehouses: {e}')
        finally:
            cur.close()
            conn.close()            
            
            
login_window()
