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