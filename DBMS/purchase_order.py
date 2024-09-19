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