def open_warehouse():
    def add_warehouse():
        # Add a new warehouse to the database
        warehouse_id = warehouse_id_entry.get()
        warehouse_name = warehouse_name_entry.get()
        location = location_entry.get()

        if not (warehouse_id and warehouse_name and location):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Warehouse (WarehouseID, WarehouseName, Location) VALUES (%s, %s, %s)",
                            (warehouse_id, warehouse_name, location))
                conn.commit()
                messagebox.showinfo('Success', 'Warehouse added successfully')
                show_win.destroy()
                open_warehouse()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding warehouse: {e}')
            finally:
                cur.close()
                conn.close()

    def update_warehouse():
        # Update selected warehouse in the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a warehouse to update')
            return

        warehouse_id = warehouse_id_entry.get()
        warehouse_name = warehouse_name_entry.get()
        location = location_entry.get()

        if not (warehouse_id and warehouse_name and location):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_warehouse_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Warehouse SET WarehouseID=%s, WarehouseName=%s, Location=%s 
                            WHERE WarehouseID=%s""",
                            (warehouse_id, warehouse_name, location, selected_warehouse_id))
                conn.commit()
                messagebox.showinfo('Success', 'Warehouse updated successfully')
                show_win.destroy()
                open_warehouse()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating warehouse: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_warehouse():
        # Delete selected warehouse from the database
        selected_item = inventory.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select a warehouse to delete')
            return

        selected_warehouse_id = inventory.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Warehouse WHERE WarehouseID=%s", (selected_warehouse_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Warehouse deleted successfully')
                show_win.destroy()
                open_warehouse()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting warehouse: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    show_win = tk.Toplevel()
    show_win.title("Warehouse List")

    # Create Treeview for displaying warehouses
    inventory = ttk.Treeview(show_win, columns=('WarehouseID', 'WarehouseName', 'Location'), show='headings')
    inventory.heading('WarehouseID', text='WarehouseID')
    inventory.heading('WarehouseName', text='WarehouseName')
    inventory.heading('Location', text='Location')
    inventory.pack(side=tk.LEFT, fill='both', expand=True)

    # Form for warehouse input
    form_frame = tk.Frame(show_win)
    form_frame.pack(side=tk.RIGHT, fill='both', expand=True)

    tk.Label(form_frame, text="WarehouseID:").grid(row=0, column=0)
    warehouse_id_entry = tk.Entry(form_frame)
    warehouse_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="WarehouseName:").grid(row=1, column=0)
    warehouse_name_entry = tk.Entry(form_frame)
    warehouse_name_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Location:").grid(row=2, column=0)
    location_entry = tk.Entry(form_frame)
    location_entry.grid(row=2, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Warehouse", command=add_warehouse)
    add_button.grid(row=3, column=0, padx=5, pady=5)

    update_button = tk.Button(form_frame, text="Update Warehouse", command=update_warehouse)
    update_button.grid(row=3, column=1, padx=5, pady=5)

    delete_button = tk.Button(form_frame, text="Delete Warehouse", command=delete_warehouse)
    delete_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Populate the Treeview with warehouse data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Warehouse")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                inventory.insert('', 'end', text=idx, values=(row[0], row[1], row[2]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving warehouses: {e}')
        finally:
            cur.close()
            conn.close()