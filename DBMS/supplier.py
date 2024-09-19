def show_suppliers():
    def add_supplier():
        # Add a new supplier to the database
        supplier_id = supplier_id_entry.get()
        supplier_name = supplier_name_entry.get()
        contact_name = contact_name_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        postal_code = postal_code_entry.get()
        country = country_entry.get()
        phone = phone_entry.get()

        if not (supplier_id and supplier_name and contact_name and address and city and postal_code and country and phone):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Supplier (SupplierID, SupplierName, ContactName, Address, City, PostalCode, Country, Phone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                            (supplier_id, supplier_name, contact_name, address, city, postal_code, country, phone))
                conn.commit()
                messagebox.showinfo('Success', 'Supplier added successfully')
                show_win.destroy()
                show_suppliers()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding supplier: {e}')
            finally:
                cur.close()
                conn.close()

    def update_supplier():
        # Update selected supplier in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a supplier to update')
            return

        supplier_id = supplier_id_entry.get()
        supplier_name = supplier_name_entry.get()
        contact_name = contact_name_entry.get()
        address = address_entry.get()
        city = city_entry.get()
        postal_code = postal_code_entry.get()
        country = country_entry.get()
        phone = phone_entry.get()

        if not (supplier_id and supplier_name and contact_name and address and city and postal_code and country and phone):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_supplier_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Supplier SET SupplierID=%s, SupplierName=%s, ContactName=%s, Address=%s, City=%s, PostalCode=%s, Country=%s, Phone=%s WHERE SupplierID=%s""",
                            (supplier_id, supplier_name, contact_name, address, city, postal_code, country, phone, selected_supplier_id))
                conn.commit()
                messagebox.showinfo('Success', 'Supplier updated successfully')
                show_win.destroy()
                show_suppliers()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating supplier: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_supplier():
        # Delete selected supplier from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a supplier to delete')
            return

        selected_supplier_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Supplier WHERE SupplierID=%s", (selected_supplier_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Supplier deleted successfully')
                show_win.destroy()
                show_suppliers()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting supplier: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    show_win = tk.Toplevel()
    show_win.title("Supplier List")

    # Create Treeview for displaying suppliers
    inventory = ttk.Treeview(show_win, columns=('SupplierID', 'SupplierName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone'), show='headings')
    inventory.heading('SupplierID', text='SupplierID')
    inventory.heading('SupplierName', text='SupplierName')
    inventory.heading('ContactName', text='ContactName')
    inventory.heading('Address', text='Address')
    inventory.heading('City', text='City')
    inventory.heading('PostalCode', text='PostalCode')
    inventory.heading('Country', text='Country')
    inventory.heading('Phone', text='Phone')
    inventory.pack(side=tk.TOP, fill='both', expand=True)  # Treeview at the top

    # Form for supplier input
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.BOTTOM, fill='x', padx=10)  # Form at the bottom

    tk.Label(form_frame, text="SupplierID:").grid(row=0, column=0, sticky='w')
    supplier_id_entry = tk.Entry(form_frame)
    supplier_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="SupplierName:").grid(row=1, column=0, sticky='w')
    supplier_name_entry = tk.Entry(form_frame)
    supplier_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="ContactName:").grid(row=2, column=0, sticky='w')
    contact_name_entry = tk.Entry(form_frame)
    contact_name_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Address:").grid(row=3, column=0, sticky='w')
    address_entry = tk.Entry(form_frame)
    address_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="City:").grid(row=4, column=0, sticky='w')
    city_entry = tk.Entry(form_frame)
    city_entry.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="PostalCode:").grid(row=5, column=0, sticky='w')
    postal_code_entry = tk.Entry(form_frame)
    postal_code_entry.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Country:").grid(row=6, column=0, sticky='w')
    country_entry = tk.Entry(form_frame)
    country_entry.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Phone:").grid(row=7, column=0, sticky='w')
    phone_entry = tk.Entry(form_frame)
    phone_entry.grid(row=7, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Supplier", command=add_supplier)
    add_button.grid(row=8, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Supplier", command=update_supplier)
    update_button.grid(row=8, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Supplier", command=delete_supplier)
    delete_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


    # Populate the Treeview with supplier data
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