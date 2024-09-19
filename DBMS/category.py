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