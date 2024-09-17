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
def open_orders_window():
    orders_win = Toplevel()
    orders_win.geometry('800x600')
    orders_win.title('Manage Orders')

    # Create a Frame for the Treeview
    treeview_frame = Frame(orders_win)
    treeview_frame.pack(fill='both', expand=True)

    # Create the Treeview
    tree = ttk.Treeview(treeview_frame, columns=("OrderID", "CustomerID", "OrderDate", "TotalAmount"), show='headings')
    tree.heading("OrderID", text="Order ID")
    tree.heading("CustomerID", text="Customer ID")
    tree.heading("OrderDate", text="Order Date")
    tree.heading("TotalAmount", text="Total Amount")
    tree.pack(fill=BOTH, expand=True)

    # Fetch and insert data
    orders = fetch_data("SELECT * FROM Orders")
    for order in orders:
        tree.insert("", END, values=order)

    # Buttons
    Button(orders_win, text='Add Order', command=add_order).pack(pady=10)
    Button(orders_win, text='Update Order', command=update_order).pack(pady=10)
    Button(orders_win, text='Delete Order', command=delete_order).pack(pady=10)
    Button(orders_win, text='Show Orders', command=lambda: update_treeview(tree, "SELECT * FROM Orders")).pack(pady=10)
def add_order():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    customer_id = simpledialog.askinteger("Input", "Enter customer ID:")
    order_date = simpledialog.askstring("Input", "Enter order date (YYYY-MM-DD):")
    total_amount = simpledialog.askfloat("Input", "Enter total amount:")
    query = "INSERT INTO Orders (CustomerID, OrderDate, TotalAmount) VALUES (%s, %s, %s)"
    cursor.execute(query, (customer_id, order_date, total_amount))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    messagebox.showinfo("Success", "Order added successfully!")

# Function to update an order
def update_order():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    order_id = simpledialog.askinteger("Input", "Enter order ID to update:")
    new_customer_id = simpledialog.askinteger("Input", "Enter new customer ID:")
    new_order_date = simpledialog.askstring("Input", "Enter new order date (YYYY-MM-DD):")
    new_total_amount = simpledialog.askfloat("Input", "Enter new total amount:")
    query = "UPDATE Orders SET CustomerID = %s, OrderDate = %s, TotalAmount = %s WHERE OrderID = %s"
    cursor.execute(query, (new_customer_id, new_order_date, new_total_amount, order_id))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    messagebox.showinfo("Success", "Order updated successfully!")

# Function to delete an order
def delete_order():
    db_conn = get_db_connection()
    cursor = db_conn.cursor()
    order_id = simpledialog.askinteger("Input", "Enter order ID to delete:")
    query = "DELETE FROM Orders WHERE OrderID = %s"
    cursor.execute(query, (order_id,))
    db_conn.commit()
    cursor.close()
    db_conn.close()
    messagebox.showinfo("Success", "Order deleted successfully!")