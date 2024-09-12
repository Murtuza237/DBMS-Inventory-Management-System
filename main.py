from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from turtle import bgcolor
from PIL import Image, ImageTk
from tkinter import filedialog
import csv
import mysql.connector  
import subprocess
from datetime import date

def main_app():
    global root
    root = Tk()
    root.geometry('1280x720')
    root.title('Inventory Management System')

    # Treeview for displaying inventory
    global inventory
    inventory = ttk.Treeview(root, columns=('ID', 'Name', 'Category', 'Quantity', 'Price'), show='headings')
    inventory.heading('ID', text='ID')
    inventory.heading('Name', text='Name')
    inventory.heading('Category', text='Category')
    inventory.heading('Quantity', text='Quantity')
    inventory.heading('Price', text='Price')
    inventory.pack(fill='both', expand=True)

    # Buttons for various functions
    Button(root, text='Connect to Database', command=connect_db).pack(pady=10)
    Button(root, text='Add Item', command=add_item).pack(pady=10)
    Button(root, text='Search Item', command=search_item).pack(pady=10)
    Button(root, text='Delete Item', command=delete_item).pack(pady=10)
    Button(root, text='Update Item', command=update_item).pack(pady=10)

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

# Function to add an item to the inventory
def add_item():
    def save_item():
        item_name = nameE.get()
        category = categoryE.get()
        quantity = quantityE.get()
        price = priceE.get()

        if item_name == '' or category == '' or quantity == '' or price == '':
            messagebox.showerror('Input Error', 'Please fill out all fields!')
        else:
            try:
                cur.execute("INSERT INTO inventory (ItemName, Category, Quantity, Price) VALUES (%s, %s, %s, %s)",
                            (item_name, category, int(quantity), float(price)))
                conn.commit()
                messagebox.showinfo('Success', 'Item added successfully!')
                addwin.destroy()
                show_items()
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding item: {e}')

    addwin = Toplevel()
    addwin.geometry('300x340')
    addwin.resizable(False, False)
    addwin.title('Add Item')

    Label(addwin, text='Item Name').pack(pady=5)
    nameE = Entry(addwin)
    nameE.pack(pady=5)

    Label(addwin, text='Category').pack(pady=5)
    categoryE = Entry(addwin)
    categoryE.pack(pady=5)

    Label(addwin, text='Quantity').pack(pady=5)
    quantityE = Entry(addwin)
    quantityE.pack(pady=5)

    Label(addwin, text='Price').pack(pady=5)
    priceE = Entry(addwin)
    priceE.pack(pady=5)

    Button(addwin, text='Save Item', command=save_item).pack(pady=20)

# Function to show all items in the Treeview
def show_items():
    for row in inventory.get_children():
        inventory.delete(row)
    try:
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()
        for idx, row in enumerate(rows, 1):
            inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4]))
    except Exception as e:
        messagebox.showerror('Database Error', f'Error retrieving inventory: {e}')

# Function to search for inventory items
def search_item():
    def perform_search():
        search_name = nameE.get()
        search_category = categoryE.get()
        search_quantity_min = quantity_minE.get()
        search_quantity_max = quantity_maxE.get()

        query = "SELECT * FROM inventory WHERE 1=1"
        params = []

        if search_name:
            query += " AND ItemName LIKE %s"
            params.append(f"%{search_name}%")
        if search_category:
            query += " AND Category LIKE %s"
            params.append(f"%{search_category}%")
        if search_quantity_min:
            query += " AND Quantity >= %s"
            params.append(int(search_quantity_min))
        if search_quantity_max:
            query += " AND Quantity <= %s"
            params.append(int(search_quantity_max))

        try:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            inventory.delete(*inventory.get_children())
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error searching inventory: {e}')

    search_win = Toplevel()
    search_win.geometry('400x300')
    search_win.resizable(False, False)
    search_win.title('Search Item')

    Label(search_win, text='Item Name').pack(pady=5)
    nameE = Entry(search_win)
    nameE.pack(pady=5)

    Label(search_win, text='Category').pack(pady=5)
    categoryE = Entry(search_win)
    categoryE.pack(pady=5)

    Label(search_win, text='Quantity Min').pack(pady=5)
    quantity_minE = Entry(search_win)
    quantity_minE.pack(pady=5)

    Label(search_win, text='Quantity Max').pack(pady=5)
    quantity_maxE = Entry(search_win)
    quantity_maxE.pack(pady=5)

    Button(search_win, text='Search', command=perform_search).pack(pady=20)
# Function to show all items in the Treeview
def show_items():
    for row in inventory.get_children():
        inventory.delete(row)

    try:
        cur.execute("SELECT * FROM inventory")
        rows = cur.fetchall()
        for idx, row in enumerate(rows, 1):
            inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4]))
    except Exception as e:
        messagebox.showerror('Database Error', f'Error retrieving inventory: {e}')

# Function to search for inventory items based on criteria
def search_item():
    def perform_search():
        search_name = nameE.get()
        search_category = categoryE.get()
        search_quantity_min = quantity_minE.get()
        search_quantity_max = quantity_maxE.get()

        query = "SELECT * FROM inventory WHERE 1=1"
        params = []

        if search_name:
            query += " AND ItemName LIKE %s"
            params.append(f"%{search_name}%")
        if search_category:
            query += " AND Category LIKE %s"
            params.append(f"%{search_category}%")
        if search_quantity_min:
            query += " AND Quantity >= %s"
            params.append(int(search_quantity_min))
        if search_quantity_max:
            query += " AND Quantity <= %s"
            params.append(int(search_quantity_max))

        try:
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            inventory.delete(*inventory.get_children())
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3], row[4]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error searching inventory: {e}')

    search_win = Toplevel()
    search_win.geometry('400x300')
    search_win.resizable(False, False)
    search_win.title('Search Item')

    Label(search_win, text='Item Name').pack(pady=5)
    nameE = Entry(search_win)
    nameE.pack(pady=5)

    Label(search_win, text='Category').pack(pady=5)
    categoryE = Entry(search_win)
    categoryE.pack(pady=5)

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
        item_id = item_idE.get()

        if item_id == '':
            messagebox.showerror('Input Error', 'Please enter an Item ID!')
        else:
            try:
                cur.execute("SELECT * FROM inventory WHERE ItemID = %s", (item_id,))
                result = cur.fetchone()

                if result:
                    confirm = messagebox.askyesno('Confirm Delete', f'Are you sure you want to delete the item with ID {item_id}?')
                    if confirm:
                        cur.execute("DELETE FROM inventory WHERE ItemID = %s", (item_id,))
                        conn.commit()
                        messagebox.showinfo('Success', 'Item deleted successfully!')
                        delete_win.destroy()
                        show_items()  # Refresh the inventory list after deletion
                    else:
                        delete_win.destroy()
                else:
                    messagebox.showerror('Error', f'No item found with ID {item_id}')
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting item: {e}')

    delete_win = Toplevel()
    delete_win.geometry('300x150')
    delete_win.resizable(False, False)
    delete_win.title('Delete Item')

    Label(delete_win, text='Enter Item ID').pack(pady=10)
    item_idE = Entry(delete_win)
    item_idE.pack(pady=5)

    Button(delete_win, text='Delete Item', command=perform_delete).pack(pady=20)

# Function to update an inventory item in the database
def update_item():
    def fetch_item():
        item_id = item_idE.get()
        if item_id == '':
            messagebox.showerror('Input Error', 'Please enter the Item ID!')
        else:
            try:
                cur.execute("SELECT * FROM inventory WHERE ItemID = %s", (item_id,))
                row = cur.fetchone()
                if row:
                    nameE.delete(0, END)
                    nameE.insert(0, row[1])
                    categoryE.delete(0, END)
                    categoryE.insert(0, row[2])
                    quantityE.delete(0, END)
                    quantityE.insert(0, row[3])
                    priceE.delete(0, END)
                    priceE.insert(0, row[4])
                else:
                    messagebox.showerror('Not Found', 'No item found with that ID!')
            except Exception as e:
                messagebox.showerror('Database Error', f'Error fetching item: {e}')

    def save_update():
        item_id = item_idE.get()
        item_name = nameE.get()
        category = categoryE.get()
        quantity = quantityE.get()
        price = priceE.get()

        if item_name == '' or category == '' or quantity == '' or price == '':
            messagebox.showerror('Input Error', 'Please fill out all fields!')
        else:
            try:
                cur.execute(
                    "UPDATE inventory SET ItemName = %s, Category = %s, Quantity = %s, Price = %s WHERE ItemID = %s",
                    (item_name, category, int(quantity), float(price), item_id)
                )
                conn.commit()
                messagebox.showinfo('Success', 'Item updated successfully!')
                update_win.destroy()
                show_items()  # Refresh the inventory list after updating
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating item: {e}')

    update_win = Toplevel()
    update_win.geometry('300x300')
    update_win.resizable(False, False)
    update_win.title('Update Item')

    Label(update_win, text='Item ID').pack(pady=5)
    item_idE = Entry(update_win)
    item_idE.pack(pady=5)

    Button(update_win, text='Fetch Item', command=fetch_item).pack(pady=10)

    Label(update_win, text='Item Name').pack(pady=5)
    nameE = Entry(update_win)
    nameE.pack(pady=5)

    Label(update_win, text='Category').pack(pady=5)
    categoryE = Entry(update_win)
    categoryE.pack(pady=5)

    Label(update_win, text='Quantity').pack(pady=5)
    quantityE = Entry(update_win)
    quantityE.pack(pady=5)

    Label(update_win, text='Price').pack(pady=5)
    priceE = Entry(update_win)
    priceE.pack(pady=5)

    Button(update_win, text='Save Update', command=save_update).pack(pady=20)

'''def low_stock_alert():
    try:
        cur.execute("SELECT ProductID, ProductName, Quantity_In_Stock, Reorder_Level FROM Product WHERE Quantity_In_Stock <= Reorder_Level")
        low_stock_items = cur.fetchall()
        
        if low_stock_items:
            alert_message = ""
            for item in low_stock_items:
                alert_message += f"Low stock alert: {item[1]} (ID: {item[0]}) has only {item[2]} items left, reorder at {item[3]}.\n"
            messagebox.showinfo("Low Stock Alert", alert_message)
        else:
            messagebox.showinfo("Low Stock Alert", "All products have sufficient stock.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error in retrieving low stock items: {e}")

def audit_product():
    product_id = product_id_entry.get()
    quantity_checked = quantity_entry.get()
    remarks = remarks_entry.get()
    
    try:
        audit_date = date.today()
        cur.execute("INSERT INTO Inventory_Audit (ProductID, Audit_Date, Quantity_Checked, Remarks) VALUES (%s, %s, %s, %s)", 
                    (product_id, audit_date, quantity_checked, remarks))
        conn.commit()
        messagebox.showinfo("Success", "Audit recorded successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error in auditing product: {e}")

def restock_item():
    product_id = restock_product_id_entry.get()
    quantity_needed = restock_quantity_entry.get()
    
    try:
        cur.execute("SELECT SupplierID, UnitPrice FROM Product_Supplier WHERE ProductID = %s", (product_id,))
        supplier = cur.fetchone()
        
        if supplier:
            supplier_id, unit_price = supplier

            cur.execute("INSERT INTO Purchase_Order (PurchaseDate, SupplierID, TotalAmount) VALUES (%s, %s, %s)",
                        (date.today(), supplier_id, int(quantity_needed) * unit_price))
            purchase_order_id = cur.lastrowid
            
            cur.execute("INSERT INTO Purchase_Order_Details (PurchaseOrder_ID, ProductID, Quantity, UnitPrice) VALUES (%s, %s, %s, %s)",
                        (purchase_order_id, product_id, quantity_needed, unit_price))
            conn.commit()
            messagebox.showinfo("Success", "Restock order placed successfully.")
        else:
            messagebox.showwarning("Error", "No supplier found for this product.")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error in placing restock order: {e}")

def sales_report():
    start_date = start_date_entry.get()
    end_date = end_date_entry.get()
    
    try:
        cur.execute("SELECT OrderDate, SUM(TotalAmount) FROM `Order` WHERE OrderDate BETWEEN %s AND %s GROUP BY OrderDate",
                    (start_date, end_date))
        sales = cur.fetchall()
        
        report_message = f"Sales Report from {start_date} to {end_date}:\n"
        for sale in sales:
            report_message += f"Date: {sale[0]}, Total Sales: {sale[1]}\n"
        
        messagebox.showinfo("Sales Report", report_message)
    
    except Exception as e:
        messagebox.showerror("Error", f"Error generating sales report: {e}")

# Creating the main application window
app = Tk.tk()
app.title("Inventory Management System")
app.geometry("400x500")

# Creating buttons to trigger each function

# Low Stock Alert Button
low_stock_button = Tk.Button(app, text="Low Stock Alert", command=low_stock_alert)
low_stock_button.pack(pady=10)

# Audit Product Button
audit_label = Tk.Label(app, text="Audit Product")
audit_label.pack()

product_id_entry = Tk.Entry(app, placeholder="Product ID")
product_id_entry.pack(pady=5)

quality_entry_pack = restock

'''