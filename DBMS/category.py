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

    # Show categories in a new window (optional function)
    def show_category():
        show_win = Toplevel()
        show_win.title("Category List")

        inventory = ttk.Treeview(show_win, columns=('CategoryID', 'CategoryName', 'Description'), show='headings')
        inventory.heading('CategoryID', text='CategoryID')
        inventory.heading('CategoryName', text='CategoryName')
        inventory.heading('Description', text='Description')
        inventory.pack(side=RIGHT, fill='both', expand=True)

        conn = get_db_connection()
        '''if conn:
            cur = conn.cursor()
            try:
                cur.execute("SELECT * FROM Category")
                rows = cur.fetchall()
                for idx, row in enumerate(rows, 1):
                    inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2]))
            except Exception as e:
                messagebox.showerror('Database Error', f'Error retrieving categories: {e}')
            finally:
                cur.close()
                conn.close()'''

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