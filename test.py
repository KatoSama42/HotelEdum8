import tkinter as tk
from tkinter import ttk
import mysql.connector

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
        self.fetch_data()

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

        ttk.Button(self.navigation_frame, text="First", command=self.show_first).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Previous", command=self.show_previous).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Next", command=self.show_next).grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Last", command=self.show_last).grid(row=0, column=3, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Add New", command=self.add_new).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(self.navigation_frame, text="Update", command=self.update_record).grid(row=0, column=5, padx=5, pady=5)

        # Initialize the record index
        self.current_record_index = 0
        self.show_record()

    def fetch_data(self):
        # Execute SQL query to fetch data from the hotel reservations table
        self.cursor.execute("SELECT * FROM hotel_reservations")
        self.records = self.cursor.fetchall()

    def show_record(self):
        # Display the current record in the form
        if self.records:
            current_record = self.records[self.current_record_index]
            self.reservation_number_var.set(current_record[0])
            self.room_number_var.set(current_record[1])
            self.check_in_var.set(current_record[2])
            self.check_out_var.set(current_record[3])
            self.customer_firstname_var.set(current_record[4])
            self.customer_lastname_var.set(current_record[5])

            # Update the title with the current reservation number
            self.root.title(f"Hotel Reservation System - Reservation Number: {current_record[0]}")

    def show_first(self):
        # Show the first record
        if self.records:
            self.current_record_index = 0
            self.show_record()

    def show_previous(self):
        # Show the previous record
        if self.current_record_index > 0:
            self.current_record_index -= 1
            self.show_record()

    def show_next(self):
        # Show the next record
        if self.current_record_index < len(self.records) - 1:
            self.current_record_index += 1
            self.show_record()

    def show_last(self):
        # Show the last record
        if self.records:
            self.current_record_index = len(self.records) - 1
            self.show_record()

    def add_new(self):
        # Add a new record to the database
        new_record = (
            self.room_number_var.get(),
            self.check_in_var.get(),
            self.check_out_var.get(),
            self.customer_firstname_var.get(),
            self.customer_lastname_var.get()
        )
        self.cursor.execute("INSERT INTO hotel_reservations (room_number, check_in, check_out, customer_firstname, customer_lastname) VALUES (%s, %s, %s, %s, %s)",
                            new_record)
        self.connection.commit()

        # Fetch updated data and show the last record
        self.fetch_data()
        self.current_record_index = len(self.records) - 1
        self.show_record()

    def update_record(self):
        # Update the current record in the database
        current_record_id = self.reservation_number_var.get()
        updated_record = (
            self.room_number_var.get(),
            self.check_in_var.get(),
            self.check_out_var.get(),
            self.customer_firstname_var.get(),
            self.customer_lastname_var.get(),
            current_record_id
        )
        self.cursor.execute("UPDATE hotel_reservations SET room_number=%s, check_in=%s, check_out=%s, customer_firstname=%s, customer_lastname=%s WHERE reservation_number=%s",
                            updated_record)
        self.connection.commit()

        # Fetch updated data
        self.fetch_data()

if __name__ == "__main__":
    # Create the main Tkinter window
    root = tk.Tk()

    # Create an instance of the HotelReservationApp class
    app = HotelReservationApp(root)

    # Run the Tkinter event loop
    root.mainloop()
