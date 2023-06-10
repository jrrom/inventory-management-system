# Import database functions to use
import database as db
# Import vertically scrolled frame component
from components.vertically_scrolled_frame import *

# Import tkinter modules
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Main class containing main program and its state variables and functions
class Main:
    # Initialise state variables
    def __init__(self):
        # Create main Tk window
        self.window = tk.Tk() 
        # Set starting screen as dashboard
        self.current_screen = "dashboard"
        # Set size of window
        self.window.geometry("1000x500")
        # Set window title
        self.window.title("Inventory Management System")

        # Dashboard contains a table of all products 
        self.dashboard = self.create_dashboard()
        # History contains logs of all changes
        self.history   = self.create_history()
        # Sidebar contains buttons to switch screens and perform data manipulation
        self.sidebar   = self.create_sidebar()

    # Pack the sidebar and dashboard and start the tkinter mainloop
    def run(self):
        self.sidebar.pack(expand=False, fill='y', side='left', anchor='nw')
        self.dashboard.pack(expand=True, fill='both', side='right')
        self.window.mainloop()

    # Function to switch between dashboard screen and history screen
    def switch(self, screen):
        # Reset dashboard
        self.dashboard.destroy()
        self.dashboard = self.create_dashboard()

        # Reset history
        self.history.destroy()
        self.history = self.create_history()

        # If screen to switch to is dashboard then switch to dashboard
        if screen == "dashboard":
            self.current_screen = "dashboard"
            self.dashboard.pack(expand=True, fill='both', side='right')
        # If screen to switch to is history then switch to dashboard
        elif screen == "history":
            self.current_screen = "history"
            self.history.pack(expand=True, fill='both', side='right')
        else:
            raise Exception("The program has an unknown value of variable screen.")

    # Function to check whether a value is a float
    def validate_numeric_input(self, new_value):
        if new_value == "":
            return True
        else:
            try:
                float(new_value)
                return True
            except ValueError:
                return False

    # Function to create sidebar
    def create_sidebar(self):
        # Create sidebar frame
        sidebar = tk.Frame(self.window, bg="#496687", height=500, width=150, relief='sunken', borderwidth=2)
        sidebar.pack_propagate(0)

        # Create button to switch to dashboard screen
        dashboard_button = tk.Button(
            sidebar, bg="#FFFFFF",text="Dashboard", height=3, width=20, 
            command=lambda: self.switch("dashboard")
        )
        # Pack with padding
        dashboard_button.pack(pady=(3,0), padx=5)

        # Create button to open add product window
        insert_button = tk.Button(
            sidebar, bg="#FFFFFF",text="Add Product", height=3, width=20, 
            command=lambda: self.create_insert()
        )
        # Pack with padding
        insert_button.pack(pady=(3,0), padx=5)

        # Create button to switch to history screen
        history_button = tk.Button(
            sidebar, bg="#FFFFFF", text="History", height=3, width=20,
            command=lambda: self.switch("history")
        )
        # Pack with padding
        history_button.pack(pady=3, padx=5)

        # Create button to open change window
        change_button = tk.Button(
            sidebar, bg="#FFFFFF", text="Change", height=3, width=20,
            command=lambda: self.create_change()
        )
        # Pack with padding
        change_button.pack(pady=3, padx=5)

        # Return sidebar Frame
        return sidebar

    # Function to create a dashboard screen
    def create_dashboard(self):
        # Create outer frame
        frame = tk.Frame(self.window, bg="#DDDDDD", height=500, width=850, padx=20, pady=20)

        # Create frame with vertical scrollbars
        dashboard = VerticalScrolledFrame(frame, bg="#DDDDDD")
        # Pack the dashboard to fill full space
        dashboard.pack(fill=tk.BOTH, expand=True)

        # Function to delete a product from the database and reload the screen
        def delete_product(id: int):
            try:
                product = db.fetch_product(id)
                db.insert_log(f"Deleted the product {product[1]}.")
                db.delete_product(id)
                self.switch("dashboard")
            except Exception as exception: 
                messagebox.showerror(title="Error", message=str(exception))

        # Loop to create top row of table
        for index, item in enumerate(["I.D", "Product", "Quantity", "Retail Price", "Wholesale Price", "Delete"]):
            element = tk.Label(
                dashboard, text=item, bg="#FF7276", highlightbackground="black", highlightthickness=1, font=("Helvetica", 15),
            )
            # To pack into table grid
            element.grid(row=0, column=index, sticky=tk.NSEW)

        # Loop to create table elements, going over products in database
        for row_index, product in enumerate(db.fetch_products()): #ROWS
            # Going over data in product
            for col_index, value in enumerate(product): #COLS
                # Each data in product is turned into a label
                element = tk.Label(
                    dashboard, text=value, highlightbackground="black", highlightthickness=1, font=("Helvetica", 15)
                )
                # If even then background is white else grey
                if row_index % 2 == 0:
                    element.config(bg="#FFFFFF")
                else:
                    element.config(bg="#DDDDDD")
                # Pack into table grid
                element.grid(row=row_index + 1, column=col_index, sticky=tk.NSEW)

            # Button to delete the product
            element = tk.Button(
                dashboard, highlightbackground="black", highlightthickness=1, font=("Helvetica", 12), activebackground="red",
                command=lambda product=product: delete_product(product[0])
            )
            # Pack into table grid
            element.grid(row=row_index + 1, column=len(product), sticky=tk.NSEW)

        # Return dashboard frame     
        return frame

    # Function to create history screen
    def create_history(self):
        # Creating outer frame
        frame = tk.Frame(self.window, bg="#DDDDDD", height=500, width=850, padx=20, pady=20)

        # Creating inner frame
        history = VerticalScrolledFrame(frame, bg="#DDDDDD")
        # Packing frame to fill available space
        history.pack(fill=tk.BOTH, expand=True)

        # Loop to create table elements, going over products in database
        for row_index, log in enumerate(db.fetch_logs()):
            # Going over data in log
            for col_index, value in enumerate(log):
                # Each data in the log is turned into a label
                element = tk.Label(
                    history, justify="left" ,highlightbackground="black", highlightthickness=1, text=value, font=("Monospace", 11)
                ) 
                # If even then background is white else grey
                if row_index % 2 == 0:
                    element.config(bg="#FFFFFF")
                else:
                    element.config(bg="#DDDDDD")
                element.grid(row=row_index + 1, column=col_index, sticky=tk.NSEW)

        # Return history frame     
        return frame 

    # Function to create insert window
    def create_insert(self):
        # Create new window
        insert = tk.Toplevel(self.window, bg="#DDDDDD")
        # Set window size
        insert.geometry("400x400")

        # Create name label and name textbox to accept input
        name_label = tk.Label(insert, text="Name:", font=("Helvetica", 14))
        name_label.pack()
        name_entry = tk.Entry(insert, font=("Helvetica", 14))
        name_entry.pack()

        # Create quantity label and quantity textbox to accept input
        quantity_label = tk.Label(insert, text="Quantity:", font=("Helvetica", 14))
        quantity_label.pack()
        quantity_entry = tk.Entry(insert, validate="key", font=("Helvetica", 14))
        # Accepts only numbers
        quantity_entry.configure(validatecommand=(quantity_entry.register(self.validate_numeric_input), "%P"))
        quantity_entry.pack()

        # Create retail price label and retail price textbox to accept input
        retail_price_label = tk.Label(insert, text="Retail Price:", font=("Helvetica", 14))
        retail_price_label.pack()
        retail_price_entry = tk.Entry(insert, validate="key", font=("Helvetica", 14))
        # Accepts only numbers
        retail_price_entry.configure(validatecommand=(retail_price_entry.register(self.validate_numeric_input), "%P"))
        retail_price_entry.pack()

        # Create wholesale price label and wholesale price textbox to accept input
        wholesale_price_label = tk.Label(insert, text="Wholesale Price:", font=("Helvetica", 14))
        wholesale_price_label.pack()
        wholesale_price_entry = tk.Entry(insert, validate="key", font=("Helvetica", 14))
        # Accepts only numbers
        wholesale_price_entry.configure(validatecommand=(wholesale_price_entry.register(self.validate_numeric_input), "%P"))
        wholesale_price_entry.pack()

        # Function to handle form submissions
        def submit():
            # Get values from textboxes
            name            = name_entry.get()
            quantity        = quantity_entry.get()
            retail_price    = retail_price_entry.get()
            wholesale_price = wholesale_price_entry.get()

            try:
                # Inserts log into database
                db.insert_log(
                    "Created a product -"                 + "\n" +  
                    f"  Name            : {name}"         + "\n" +
                    f"  Quantity        : {quantity}"     + "\n" +
                    f"  Retail Price    : {retail_price}" + "\n" +
                    f"  Wholesale Price : {wholesale_price}"
                )
                # Reload history window if open and show new logs
                self.switch("history") if self.current_screen == "history" else None

                # If any textbox is empty it will throw an exception and an error message will be shown to the user
                if name == "" or quantity == "" or retail_price == "" or wholesale_price == "":
                    raise Exception("Name, quantity, retail price or wholesale price is empty.")
                # Insert product into database
                db.insert_product(name, int(quantity), float(retail_price), float(wholesale_price))
                # Delete values of textboxes now that new product has been entered into the database
                name_entry.delete(0, tk.END)
                quantity_entry.delete(0, tk.END)
                retail_price_entry.delete(0, tk.END)
                wholesale_price_entry.delete(0, tk.END)
                # Reload screen if current screen is dashboard and show new product
                self.switch("dashboard") if self.current_screen == "dashboard" else None
            except Exception as exception: 
                # If there are any exceptions, an error message will be shown to the user
                messagebox.showerror(title="Error", message=str(exception))

        # Create submit function, link it to the function and pack
        submit_button = tk.Button(insert, text="Submit", command=lambda: submit(), font=("Helvetica", 14))
        submit_button.pack()

        # Return insert window
        return insert

    # Function to create change window
    def create_change(self):
        # Create new window
        change = tk.Toplevel(self.window, bg="#DDDDDD")
        # Set new window size
        change.geometry("400x400")


        # Function to deal with changes in dropdown selection
        def selection_changed(event):
            # Turns id:name into (id, ":", name)
            selection  = (dropdown.get()).partition(":")
            # Get product id
            product_id = selection[0]

            # Get product from database
            product = db.fetch_product(product_id)

            # Delete empty name entry and replace with product name
            name_entry.delete(0, tk.END)
            name_entry.insert(0, product[1])

            # Delete empty quantity entry and replace with product quantity 
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, product[2])

            # Delete empty retail price entry and replace with product retail price
            retail_price_entry.delete(0, tk.END)
            retail_price_entry.insert(0, product[3])

            # Delete empty wholesale price entry and replace with wholesale retail price
            wholesale_price_entry.delete(0, tk.END)
            wholesale_price_entry.insert(0, product[4])

        # Create dropdown box with values consisting of products in database for user to choose to edit
        dropdown = ttk.Combobox(
            change,
            state="readonly",
            values=[f"{product[0]}:{product[1]}" for product in db.fetch_products()],
            font=("Helvetica", 14)
        )
        dropdown.pack()
        # Bind to function
        dropdown.bind("<<ComboboxSelected>>", selection_changed)

        # Create name label and textbox
        name_label = tk.Label(change, text="Name:", font=("Helvetica", 14))
        name_label.pack()
        name_entry = tk.Entry(change, font=("Helvetica", 14))
        name_entry.pack()

        # Create quantity label and textbox
        quantity_label = tk.Label(change, text="Quantity:", font=("Helvetica", 14))
        quantity_label.pack()
        quantity_entry = tk.Entry(change, validate="key", font=("Helvetica", 14))
        # Accepts only numbers
        quantity_entry.configure(validatecommand=(quantity_entry.register(self.validate_numeric_input), "%P"))
        quantity_entry.pack()

        # Create retail price label and textbox
        retail_price_label = tk.Label(change, text="Retail Price:", font=("Helvetica", 14))
        retail_price_label.pack()
        retail_price_entry = tk.Entry(change, validate="key", font=("Helvetica", 14))
        # Accepts only numbers
        retail_price_entry.configure(validatecommand=(retail_price_entry.register(self.validate_numeric_input), "%P"))
        retail_price_entry.pack()

        # Create wholesale price label and textbox
        wholesale_price_label = tk.Label(change, text="Wholesale Price:", font=("Helvetica", 14))
        wholesale_price_label.pack()
        wholesale_price_entry = tk.Entry(change, validate="key", font=("Helvetica", 14))
        # Accepts only numbers
        wholesale_price_entry.configure(validatecommand=(wholesale_price_entry.register(self.validate_numeric_input), "%P"))
        wholesale_price_entry.pack()


        # Function to handle form submissions
        def submit():
            # Get values from textboxes
            name            = name_entry.get()
            quantity        = quantity_entry.get()
            retail_price    = retail_price_entry.get()
            wholesale_price = wholesale_price_entry.get()

            try:
                # Get product id
                selection  = (dropdown.get()).partition(":")
                product_id = selection[0]

                # Get product from database before update
                product = db.fetch_product(product_id) 
                # Insert log showing changes between values
                db.insert_log(
                    f"Changed a product (id {product_id}) -"              + "\n" +
                    f"  Name            : {product[1]} ~> {name}"         + "\n" +
                    f"  Quantity        : {product[2]} ~> {quantity}"     + "\n" +
                    f"  Retail Price    : {product[3]} ~> {retail_price}" + "\n" +
                    f"  Wholesale Price : {product[4]} ~> {wholesale_price}"
                )
                # If current screen is history then reload
                self.switch("history") if self.current_screen == "history" else None

                # Any empty textbox will throw exception
                if product_id == "" or quantity == "" or retail_price == "" or wholesale_price == "":
                    raise Exception("No product selected or name, quantity, retail price or wholesale price is empty.")
                # Edit the product
                db.edit_product(product_id, name, int(quantity), float(retail_price), float(wholesale_price))
                # Reload dashboard if it is open
                self.switch("dashboard") if self.current_screen == "dashboard" else None
            # Show error in new window
            except Exception as exception: 
                messagebox.showerror(title="Error", message=str(exception))

        # Create submission button and pack
        submit_button = tk.Button(change, text="Submit", command=lambda: submit())
        submit_button.pack()

        return change 

# Main function
def main():
    # Create main class
    program = Main()
    # Run
    program.run()