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