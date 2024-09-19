def open_home_page():
    home_page = Tk()
    home_page.geometry('1280x720')
    home_page.title('Inventory Management Home Page')


    # Create a frame for the heading, place it on top of the background
    heading_label = Label(home_page, text="INVENTORY MANAGEMENT SYSTEM", font=("Helvetica", 24,BOLD), bg="white", fg='black')
    heading_label.place(relx=0.5, rely=0.1, anchor='center')  # Place it centered horizontally at 10% height

    bg_image = Image.open("/Users/murtuzaali/Downloads/DBMS Course project/WhatsApp Image 2024-09-12 at 16.04.56.png")
    bg_image = bg_image.resize((1280, 720))
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    background_label = Label(home_page, image=bg_photo)
    background_label.place(relwidth=1, relheight=1)

    frame = Frame(home_page, bg='white')
    frame.pack(side=LEFT, padx=50, pady=10)

    buttons = [
        ('Product', open_products),
        ('Order', show_orders),
        ('Supplier', show_suppliers),
        ('Customer', open_customer),
        ('Purchase Order',open_purchase_orders),
        ('Purchase Order Details',open_purchase_order_details),
        ('Category', open_category_window),
        ('Warehouse',open_warehouse),
        ('Inventory Audit',open_inventory_audit),
        ('Log out',lambda: logout(home_page))
    ]

    for text, command in buttons:
        Button(frame, text=text, width=20, height=2, command=command).pack(pady=5)

    home_page.mainloop()
    
    
def logout(home_page):
    # Ask for confirmation before logging out
    response = messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?")
    
    if response:  # If the user clicks 'Yes'
        # Close the current window
        home_page.destroy()
        # Reopen the login window (assuming you have a function called login_window)
        login_window()