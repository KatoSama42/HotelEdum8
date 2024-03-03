import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime

class HotelReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation System")

        # Database connection details
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "Nazlee24"
        self.db_name = "HotelDB"

        # Connect to the database and fetch data
        self.connection = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            database=self.db_name
        )
        self.cursor = self.connection.cursor()

        # Data entry form
        self.form_frame = ttk.Frame(self.root)
        self.form_frame.pack(pady=10)

        self.reservation_number_var = tk.StringVar()
        self.room_number_var = tk.StringVar()
        self.check_in_var = tk.StringVar()
        self.check_out_var = tk.StringVar()
        self.customer_firstname_var = tk.StringVar()
        self.customer_lastname_var = tk.StringVar()

        ttk.Label(self.form_frame, text="Room Number:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.form_frame, textvariable=self.room_number_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Check-in (dd-mm-yyyy):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.form_frame, textvariable=self.check_in_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Check-out (dd-mm-yyyy):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.form_frame, textvariable=self.check_out_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Customer First Name:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.form_frame, textvariable=self.customer_firstname_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.form_frame, text="Customer Last Name:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        ttk.Entry(self.form_frame, textvariable=self.customer_lastname_var).grid(row=4, column=1, padx=5, pady=5)

        # Navigation buttons
        self.navigation_frame = ttk.Frame(self.root)
        self.navigation_frame.pack(pady=10)


        ttk.Button(self.navigation_frame, text="Add New", command=self.add_new).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Delete", command=self.delete_record).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Update", command=self.update_record).grid(row=0, column=5, padx=5, pady=5)

        # Treeview for displaying data
        self.tree = ttk.Treeview(self.root, columns=("Reservation Number", "Room Number", "Check-in", "Check-out", "First Name", "Last Name"))
        self.tree.heading("#0", text="Reservation Number")
        self.tree.heading("Room Number", text="Room Number")
        self.tree.heading("Check-in", text="Check-in")
        self.tree.heading("Check-out", text="Check-out")
        self.tree.heading("First Name", text="First Name")
        self.tree.heading("Last Name", text="Last Name")
        self.tree.pack(pady=10)

        # Fetch and display data
        self.fetch_data()

        # Bind selection event of the treeview to update form fields
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def fetch_data(self):
        # Clear existing data in the treeview
        for record in self.tree.get_children():
            self.tree.delete(record)

        # Execute SQL query to fetch data from the hotel reservations table
        self.cursor.execute("SELECT * FROM hotel_reservations")
        records = self.cursor.fetchall()

        # Insert fetched data into the treeview
        for record in records:
            reservation_number, room_number, check_in, check_out, first_name, last_name = record
            check_in = check_in.strftime('%d-%m-%Y') if check_in else ""
            check_out = check_out.strftime('%d-%m-%Y') if check_out else ""
            self.tree.insert("", "end", text=reservation_number, values=(room_number, check_in, check_out, first_name, last_name))

    def on_tree_select(self, event):
        # Get selected item from the treeview
        selected_item = self.tree.selection()
        if selected_item:
            # Get values of the selected item
            item_values = self.tree.item(selected_item)['values']
            if item_values:
                # Fill form fields with selected item values
                self.room_number_var.set(item_values[0])
                self.check_in_var.set(item_values[1])
                self.check_out_var.set(item_values[2])
                self.customer_firstname_var.set(item_values[3])
                self.customer_lastname_var.set(item_values[4])


    def show_record(self):
        # Display the selected record from the treeview in the form
        selected_record = self.tree.selection()
        if selected_record:
            record = self.tree.item(selected_record[0], 'values')
            self.room_number_var.set(record[0])
            self.check_in_var.set(record[1])
            self.check_out_var.set(record[2])
            self.customer_firstname_var.set(record[3])
            self.customer_lastname_var.set(record[4])

    def add_new(self):
        # Add a new record to the database
        new_record = (
            self.room_number_var.get(),
            datetime.strptime(self.check_in_var.get(), '%d-%m-%Y').date() if self.check_in_var.get() else None,
            datetime.strptime(self.check_out_var.get(), '%d-%m-%Y').date() if self.check_out_var.get() else None,
            self.customer_firstname_var.get(),
            self.customer_lastname_var.get()
        )
        self.cursor.execute("INSERT INTO hotel_reservations (room_number, check_in, check_out, customer_firstname, customer_lastname) VALUES (%s, %s, %s, %s, %s)",
                            new_record)
        self.connection.commit()

        # Fetch updated data and refresh the treeview
        self.fetch_data()
    def delete_record(self):
        # Get selected item from the treeview
        selected_item = self.tree.selection()
        if selected_item:
            # Get reservation number of the selected item
            reservation_number = self.tree.item(selected_item[0])['text']
            # Execute SQL query to delete the record
            self.cursor.execute("DELETE FROM hotel_reservations WHERE reservation_number = %s", (reservation_number,))
            self.connection.commit()
            # Refresh the treeview
            self.fetch_data()
    def update_record(self):
        # Update the selected record in the database
        selected_record = self.tree.selection()
        if selected_record:
            record_id = self.tree.item(selected_record[0])['text']
            updated_record = (
                self.room_number_var.get(),
                datetime.strptime(self.check_in_var.get(), '%d-%m-%Y').date() if self.check_in_var.get() else None,
                datetime.strptime(self.check_out_var.get(), '%d-%m-%Y').date() if self.check_out_var.get() else None,
                self.customer_firstname_var.get(),
                self.customer_lastname_var.get(),
                record_id
            )
            self.cursor.execute("UPDATE hotel_reservations SET room_number=%s, check_in=%s, check_out=%s, customer_firstname=%s, customer_lastname=%s WHERE reservation_number=%s",
                                updated_record)
            self.connection.commit()

            # Refresh the treeview
            self.fetch_data()

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()

    # Create an instance of the HotelReservationApp class
    app = HotelReservationApp(root)

    # Run the Tkinter event loop
    root.mainloop()
