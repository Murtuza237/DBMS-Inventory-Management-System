def show_orders():
    def add_order():
        order_id = order_id_entry.get()
        customer_id = customer_id_entry.get()
        order_date = order_date_entry.get()
        total_amount = total_amount_entry.get()

        if not (order_id and customer_id and order_date and total_amount):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount) VALUES (%s, %s, %s, %s)",
                            (order_id, customer_id, order_date, total_amount))
                conn.commit()
                messagebox.showinfo('Success', 'Order added successfully')
                orders_win.destroy()
                show_orders()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error adding order: {e}')
            finally:
                cur.close()
                conn.close()

    def update_order():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order to update')
            return

        order_id = order_id_entry.get()
        customer_id = customer_id_entry.get()
        order_date = order_date_entry.get()
        total_amount = total_amount_entry.get()

        if not (order_id and customer_id and order_date and total_amount):
            messagebox.showwarning('Input Error', 'Please fill in all fields')
            return

        selected_order_id = tree.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("""UPDATE Orders SET OrderID=%s, CustomerID=%s, OrderDate=%s, TotalAmount=%s WHERE OrderID=%s""",
                            (order_id, customer_id, order_date, total_amount, selected_order_id))
                conn.commit()
                messagebox.showinfo('Success', 'Order updated successfully')
                orders_win.destroy()
                show_orders()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error updating order: {e}')
            finally:
                cur.close()
                conn.close()

    def delete_order():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning('Selection Error', 'Please select an order to delete')
            return

        selected_order_id = tree.item(selected_item[0])['values'][0]

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute("DELETE FROM Orders WHERE OrderID=%s", (selected_order_id,))
                conn.commit()
                messagebox.showinfo('Success', 'Order deleted successfully')
                orders_win.destroy()
                show_orders()  # Refresh the window
            except Exception as e:
                messagebox.showerror('Database Error', f'Error deleting order: {e}')
            finally:
                cur.close()
                conn.close()

    # Create the window
    orders_win = tk.Toplevel()
    orders_win.geometry('800x600')
    orders_win.title('Manage Orders')

    # Create a Frame for the Treeview
    treeview_frame = tk.Frame(orders_win)
    treeview_frame.pack(side=tk.TOP, fill='both', expand=True)

    # Create the Treeview
    tree = ttk.Treeview(treeview_frame, columns=("OrderID", "CustomerID", "OrderDate", "TotalAmount"), show='headings')
    tree.heading("OrderID", text="Order ID")
    tree.heading("CustomerID", text="Customer ID")
    tree.heading("OrderDate", text="Order Date")
    tree.heading("TotalAmount", text="Total Amount")
    tree.pack(fill='both', expand=True)

    # Form for order input
    form_frame = tk.Frame(orders_win)
    form_frame.pack(side=tk.BOTTOM, fill='x')

    tk.Label(form_frame, text="Order ID:").grid(row=0, column=0, sticky='w')
    order_id_entry = tk.Entry(form_frame)
    order_id_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Customer ID:").grid(row=1, column=0, sticky='w')
    customer_id_entry = tk.Entry(form_frame)
    customer_id_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Order Date (YYYY-MM-DD):").grid(row=2, column=0, sticky='w')
    order_date_entry = tk.Entry(form_frame)
    order_date_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Total Amount:").grid(row=3, column=0, sticky='w')
    total_amount_entry = tk.Entry(form_frame)
    total_amount_entry.grid(row=3, column=1, padx=5, pady=5)

    # Buttons for Add, Update, and Delete
    add_button = tk.Button(form_frame, text="Add Order", command=add_order)
    add_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

    update_button = tk.Button(form_frame, text="Update Order", command=update_order)
    update_button.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

    delete_button = tk.Button(form_frame, text="Delete Order", command=delete_order)
    delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')


    # Populate the Treeview with order data
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute("SELECT * FROM Orders")
            rows = cur.fetchall()
            for idx, row in enumerate(rows, 1):
                tree.insert('', 'end', text=idx, values=(row[0], row[1], row[2], row[3]))
        except Exception as e:
            messagebox.showerror('Database Error', f'Error retrieving orders: {e}')
        finally:
            cur.close()
            conn.close()