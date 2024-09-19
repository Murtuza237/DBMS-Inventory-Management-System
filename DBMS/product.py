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