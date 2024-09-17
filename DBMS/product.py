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
def open_product_window():
    product_win = Tk()
    product_win.geometry('1280x720')
    product_win.title('Manage Products')

    # Create a Frame for the Treeview and Buttons
    main_frame = Frame(product_win)
    main_frame.pack(fill='both', expand=True)

    # Create a Frame for the Treeview
    treeview_frame = Frame(main_frame)
    treeview_frame.grid(row=0, column=0, columnspan=2)

    # Create the Treeview
    global inventory
    inventory = ttk.Treeview(treeview_frame, columns=('ProductID', 'ProductName', 'CategoryID', 'Quantity_In_Stock', 'Reorder_Level', 'UnitPrice', 'SupplierID'), show='headings')
    inventory.heading('ProductID', text='ProductID')
    inventory.heading('ProductName', text='ProductName')
    inventory.heading('CategoryID', text='CategoryID')
    inventory.heading('Quantity_In_Stock', text='Quantity_In_Stock')
    inventory.heading('Reorder_Level', text='Reorder_Level')
    inventory.heading('UnitPrice', text='UnitPrice')
    inventory.heading('SupplierID', text='SupplierID')
    inventory.pack(side=TOP, fill='both', expand=True)

    # Create a Frame for the Buttons
    button_frame = Frame(main_frame)
    button_frame.grid(row=1, column=0, columnspan=2, sticky='ew')

    # Add Buttons to the Button Frame
    Button(button_frame, text='Add Product', command=add_product).pack(pady=10)
    Button(button_frame, text='Update Product', command=update_product).pack(pady=10)
    Button(button_frame, text='Delete Product', command=delete_product).pack(pady=10)
    Button(button_frame, text='Show Products', command=lambda: show_products(inventory, "SELECT * FROM Supplier")).pack(pady=10)

    # Configure grid weights
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(0, weight=3)
    main_frame.grid_rowconfigure(1, weight=1)

    product_win.mainloop()
    
    def show_products():
        show_win = Toplevel()
        show_win.title("Product List")

        inventory = ttk.Treeview(show_win, columns=('ProductID', 'ProductName', 'CategoryID', 'Quantity_In_Stock', 'Reorder_Level', 'UnitPrice', 'SupplierID'), show='headings')
        inventory.heading('ProductID', text='ProductID')
        inventory.heading('ProductName', text='ProductName')
        inventory.heading('CategoryID', text='CategoryID')
        inventory.heading('Quantity_In_Stock', text='Quantity_In_Stock')
        inventory.heading('Reorder_Level', text='Reorder_Level')
        inventory.heading('UnitPrice', text='UnitPrice')
        inventory.heading('SupplierID', text='SupplierID')
        inventory.pack(side=RIGHT, fill='both', expand=False)

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
        def update_treeview():
            # Clear the current contents of the treeview
            for row in inventory.get_children():
                inventory.delete(row)
            
            # Fetch the updated data and insert it into the treeview
            categories = fetch_data("SELECT * FROM Product")
            for category in categories:
                inventory.insert("", END, values=category)

    def add_product():
        def save_product():
            product_name = nameE.get()
            category_id = categoryE.get()
            unit_price = priceE.get()
            quantity = quantityE.get()
            reorder_level = reorderE.get()
            supplier_id = supplierE.get()

            if product_name == '' or category_id == '' or unit_price == '' or quantity == '' or reorder_level == '' or supplier_id == '':
                messagebox.showerror('Input Error', 'Please fill out all fields!')
            else:
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    try:
                        cur.execute("INSERT INTO Product (ProductName, CategoryID, Quantity_In_Stock, Reorder_Level, UnitPrice, SupplierID) VALUES (%s, %s, %s, %s, %s, %s)",
                                    (product_name, int(category_id), int(quantity), int(reorder_level), float(unit_price), int(supplier_id)))
                        conn.commit()
                        messagebox.showinfo('Success', 'Product added successfully!')
                        addwin.destroy()
                        show_products()
                    except Exception as e:
                        messagebox.showerror('Database Error', f'Error adding product: {e}')
                    finally:
                        cur.close()
                        conn.close()

        addwin = Toplevel()
        addwin.geometry('300x500')
        addwin.resizable(False, False)
        addwin.title('Add Product')

        Label(addwin, text='Product Name').pack(pady=5)
        nameE = Entry(addwin)
        nameE.pack(pady=5)

        Label(addwin, text='Category ID').pack(pady=5)
        categoryE = Entry(addwin)
        categoryE.pack(pady=5)

        Label(addwin, text='Unit Price').pack(pady=5)
        priceE = Entry(addwin)
        priceE.pack(pady=5)

        Label(addwin, text='Quantity In Stock').pack(pady=5)
        quantityE = Entry(addwin)
        quantityE.pack(pady=5)

        Label(addwin, text='Reorder Level').pack(pady=5)
        reorderE = Entry(addwin)
        reorderE.pack(pady=5)

        Label(addwin, text='Supplier ID').pack(pady=5)
        supplierE = Entry(addwin)
        supplierE.pack(pady=5)

        Button(addwin, text='Save Product', command=save_product).pack(pady=20)

    def update_product():
        def save_update():
            product_id = product_idE.get()
            product_name = nameE.get()
            category_id = categoryE.get()
            unit_price = priceE.get()
            quantity = quantityE.get()
            reorder_level = reorderE.get()
            supplier_id = supplierE.get()

            if product_id == '' or product_name == '' or category_id == '' or unit_price == '' or quantity == '' or reorder_level == '' or supplier_id == '':
                messagebox.showerror('Input Error', 'Please fill out all fields!')
            else:
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    try:
                        cur.execute("UPDATE Product SET ProductName=%s, CategoryID=%s, Quantity_In_Stock=%s, Reorder_Level=%s, UnitPrice=%s, SupplierID=%s WHERE ProductID=%s",
                                    (product_name, int(category_id), int(quantity), int(reorder_level), float(unit_price), int(supplier_id), int(product_id)))
                        conn.commit()
                        messagebox.showinfo('Success', 'Product updated successfully!')
                        update_win.destroy()
                        show_products()
                    except Exception as e:
                        messagebox.showerror('Database Error', f'Error updating product: {e}')
                    finally:
                        cur.close()
                        conn.close()

        update_win = Toplevel()
        update_win.geometry('300x550')
        update_win.resizable(False, False)
        update_win.title('Update Product')

        Label(update_win, text='Product ID').pack(pady=5)
        product_idE = Entry(update_win)
        product_idE.pack(pady=5)

        Label(update_win, text='Product Name').pack(pady=5)
        nameE = Entry(update_win)
        nameE.pack(pady=5)

        Label(update_win, text='Category ID').pack(pady=5)
        categoryE = Entry(update_win)
        categoryE.pack(pady=5)

        Label(update_win, text='Unit Price').pack(pady=5)
        priceE = Entry(update_win)
        priceE.pack(pady=5)

        Label(update_win, text='Quantity In Stock').pack(pady=5)
        quantityE = Entry(update_win)
        quantityE.pack(pady=5)

        Label(update_win, text='Reorder Level').pack(pady=5)
        reorderE = Entry(update_win)
        reorderE.pack(pady=5)

        Label(update_win, text='Supplier ID').pack(pady=5)
        supplierE = Entry(update_win)
        supplierE.pack(pady=5)

        Button(update_win, text='Save Changes', command=save_update).pack(pady=20)


    def delete_product():
        def confirm_delete():
            product_id = product_idE.get()

            if product_id == '':
                messagebox.showerror('Input Error', 'Please enter the Product ID!')
            else:
                conn = get_db_connection()
                if conn:
                    cur = conn.cursor()
                    try:
                        cur.execute("DELETE FROM Product WHERE ProductID=%s", (product_id,))
                        conn.commit()
                        messagebox.showinfo('Success', 'Product deleted successfully!')
                        delete_win.destroy()
                        show_products()
                    except Exception as e:
                        messagebox.showerror('Database Error', f'Error deleting product: {e}')
                    finally:
                        cur.close()
                        conn.close()

        delete_win = Toplevel()
        delete_win.geometry('300x200')
        delete_win.resizable(False, False)
        delete_win.title('Delete Product')

        Label(delete_win, text='Product ID').pack(pady=20)
        product_idE = Entry(delete_win)
        product_idE.pack(pady=5)

        Button(delete_win, text='Delete Product', command=confirm_delete).pack(pady=20)