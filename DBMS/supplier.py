from tkinter import *
from tkinter import messagebox,simpledialog
from tkinter import ttk
from tkinter.font import BOLD
from PIL import Image, ImageTk
import mysql.connector

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

def fetch_data(query):
    # Establish connection to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="Murtuza",
        password="12345678",
        database="inventorymanagementsystem"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
def update_treeview(tree, query):
    for item in tree.get_children():
        tree.delete(item)
    data = fetch_data(query)
    for row in data:
        tree.insert("", END, values=row)
def open_supplier_window():
    supplier_win = Toplevel()
    supplier_win.geometry('800x600')
    supplier_win.title('Manage Suppliers')

    # Treeview setup
    tree = ttk.Treeview(supplier_win, columns=("SupplierID", "SupplierName", "ContactName", "Address", "City", "PostalCode", "Country", "Phone"), show='headings')
    tree.pack(fill=BOTH, expand=True)

    # Define column headings
    tree.heading("SupplierID", text="Supplier ID")
    tree.heading("SupplierName", text="Supplier Name")
    tree.heading("ContactName", text="Contact Name")
    tree.heading("Address", text="Address")
    tree.heading("City", text="City")
    tree.heading("PostalCode", text="Postal Code")
    tree.heading("Country", text="Country")
    tree.heading("Phone", text="Phone")

    # Fetch and insert data
    suppliers = fetch_data("SELECT * FROM Supplier")
    for supplier in suppliers:
        tree.insert("", END, values=supplier)

    # Buttons
    Button(supplier_win, text='Add Supplier', command=add_supplier).pack(pady=10)
    Button(supplier_win, text='Update Supplier', command=update_supplier).pack(pady=10)
    Button(supplier_win, text='Delete Supplier', command=delete_supplier).pack(pady=10)
    Button(supplier_win, text='Show Suppliers', command=lambda: update_treeview(tree, "SELECT * FROM Supplier")).pack(pady=10)



def show_suppliers():
    show_win = Toplevel()
    show_win.title("Supplier List")

    inventory = ttk.Treeview(show_win, columns=('SupplierID', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone'), show='headings')
    inventory.heading('SupplierID', text='SupplierID')
    inventory.heading('SupplierName', text='SupplierName')
    inventory.heading('ContactName', text='ContactName')
    inventory.heading('Address', text='Address')
    inventory.heading('City', text='City')
    inventory.heading('PostalCode', text='PostalCode')
    inventory.heading('Country', text='Country')
    inventory.heading('Phone', text='Phone')
    inventory.pack(side=RIGHT, fill='both', expand=True)

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

def add_supplier():
    def save_supplier():
        supplier_name = nameE.get()
        contact_name = contactE.get()
        address = addressE.get()
        city = cityE.get()
        postal_code = postalE.get()
        country = countryE.get()
        phone = phoneE.get()

        if supplier_name == '' or contact_name == '' or address == '' or city == '' or postal_code == '' or country == '' or phone == '':
            messagebox.showerror('Input Error', 'Please fill out all fields!')
        else:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("INSERT INTO Supplier (SupplierName, ContactName, Address, City, PostalCode, Country, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                                (supplier_name, contact_name, address, city, postal_code, country, phone))
                    conn.commit()
                    messagebox.showinfo('Success', 'Supplier added successfully!')
                    add_win.destroy()
                    show_suppliers()
                except Exception as e:
                    messagebox.showerror('Database Error', f'Error adding supplier: {e}')
                finally:
                    cur.close()
                    conn.close()

    add_win = Toplevel()
    add_win.geometry('300x550')
    add_win.resizable(False, False)
    add_win.title('Add Supplier')

    Label(add_win, text='Supplier Name').pack(pady=5)
    nameE = Entry(add_win)
    nameE.pack(pady=5)

    Label(add_win, text='Contact Name').pack(pady=5)
    contactE = Entry(add_win)
    contactE.pack(pady=5)

    Label(add_win, text='Address').pack(pady=5)
    addressE = Entry(add_win)
    addressE.pack(pady=5)

    Label(add_win, text='City').pack(pady=5)
    cityE = Entry(add_win)
    cityE.pack(pady=5)

    Label(add_win, text='Postal Code').pack(pady=5)
    postalE = Entry(add_win)
    postalE.pack(pady=5)

    Label(add_win, text='Country').pack(pady=5)
    countryE = Entry(add_win)
    countryE.pack(pady=5)

    Label(add_win, text='Phone').pack(pady=5)
    phoneE = Entry(add_win)
    phoneE.pack(pady=5)

    Button(add_win, text='Save Supplier', command=save_supplier).pack(pady=20)

def update_supplier():
    def save_update():
        supplier_id = supplier_idE.get()
        supplier_name = nameE.get()
        contact_name = contactE.get()
        address = addressE.get()
        city = cityE.get()
        postal_code = postalE.get()
        country = countryE.get()
        phone = phoneE.get()

        if supplier_id == '' or supplier_name == '' or contact_name == '' or address == '' or city == '' or postal_code == '' or country == '' or phone == '':
            messagebox.showerror('Input Error', 'Please fill out all fields!')
        else:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("UPDATE Supplier SET SupplierName=%s, ContactName=%s, Address=%s, City=%s, PostalCode=%s, Country=%s, Phone=%s WHERE SupplierID=%s",
                                (supplier_name, contact_name, address, city, postal_code, country, phone, int(supplier_id)))
                    conn.commit()
                    messagebox.showinfo('Success', 'Supplier updated successfully!')
                    update_win.destroy()
                    show_suppliers()
                except Exception as e:
                    messagebox.showerror('Database Error', f'Error updating supplier: {e}')
                finally:
                    cur.close()
                    conn.close()

    update_win = Toplevel()
    update_win.geometry('300x600')
    update_win.resizable(False, False)
    update_win.title('Update Supplier')

    Label(update_win, text='Supplier ID').pack(pady=5)
    supplier_idE = Entry(update_win)
    supplier_idE.pack(pady=5)

    Label(update_win, text='Supplier Name').pack(pady=5)
    nameE = Entry(update_win)
    nameE.pack(pady=5)

    Label(update_win, text='Contact Name').pack(pady=5)
    contactE = Entry(update_win)
    contactE.pack(pady=5)

    Label(update_win, text='Address').pack(pady=5)
    addressE = Entry(update_win)
    addressE.pack(pady=5)

    Label(update_win, text='City').pack(pady=5)
    cityE = Entry(update_win)
    cityE.pack(pady=5)

    Label(update_win, text='Postal Code').pack(pady=5)
    postalE = Entry(update_win)
    postalE.pack(pady=5)

    Label(update_win, text='Country').pack(pady=5)
    countryE = Entry(update_win)
    countryE.pack(pady=5)

    Label(update_win, text='Phone').pack(pady=5)
    phoneE = Entry(update_win)
    phoneE.pack(pady=5)

    Button(update_win, text='Save Changes', command=save_update).pack(pady=20)


def delete_supplier():
    def confirm_delete():
        supplier_id = supplier_idE.get()

        if supplier_id == '':
            messagebox.showerror('Input Error', 'Please enter the Supplier ID!')
        else:
            conn = get_db_connection()
            if conn:
                cur = conn.cursor()
                try:
                    cur.execute("DELETE FROM Supplier WHERE SupplierID=%s", (supplier_id,))
                    conn.commit()
                    messagebox.showinfo('Success', 'Supplier deleted successfully!')
                    delete_win.destroy()
                    show_suppliers()
                except Exception as e:
                    messagebox.showerror('Database Error', f'Error deleting supplier: {e}')
                finally:
                    cur.close()
                    conn.close()

    delete_win = Toplevel()
    delete_win.geometry('300x200')
    delete_win.resizable(False, False)
    delete_win.title('Delete Supplier')

    Label(delete_win, text='Supplier ID').pack(pady=20)
    supplier_idE = Entry(delete_win)
    supplier_idE.pack(pady=5)

    Button(delete_win, text='Delete Supplier', command=confirm_delete).pack(pady=20)