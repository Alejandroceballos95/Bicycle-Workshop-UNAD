"""
Course: Programming - (213023)
Phase: Phase 2 - Object-Oriented Programming Design
Exercise: 1 - Bicycle Workshop Control System
Student Name: Jhon Alejandro Ceballos Tobon
Group: 109
Date: March 2026
Description: This application manages a bicycle workshop using POO, encapsulation, and a graphical interface with Tkinter.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import json
import os

"""
CLASS: User
Description: Manages user authentication and credential persistence. Complies with Phase 2 requirements: Encapsulation and Private Attributes.
"""


class User:
    def __init__(self):
        """
        Initializes the user class.
        Sets up the file path and private attributes for security.
        """
        # File name for local data persistence.
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.__file_name = os.path.join(base_path, "user_credentials.json")

        # Private attributes (Encapsulation).
        self._username = ""
        self._password = ""

        # Load or create credentials on startup.
        self._setup_user_data()

    def _setup_user_data(self):
        """
        Checks if the JSON file exists. If not, creates it with default
        credentials 'programación'. Then loads them into memory.
        """
        if not os.path.exists(self.__file_name):
            # Default values
            default_data = {
                "username": "programación",
                "password": "programación"
            }
            # Writing to the JSON file
            with open(self.__file_name, 'w', encoding='utf-8') as file:
                json.dump(default_data, file, indent=4)

        # Reading data from the local file
        with open(self.__file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            self._username = data["username"]
            self._password = data["password"]

    def validate_credentials(self, input_user, input_pass):
        """
        Public method to verify if the providede credentials match the stored ones.
        Returns: True if successful, False otherwise.
        """
        if input_user == self._username and input_pass == self._password:
            return True
        return False


"""
CLASS: BicycleWorkshop
Description: Manages the logic for a single bicycle service.
"""


class BicycleWorkshop:
    def __init__(self, serial, entry_hour, hour_rate):
        # Private attributes for encapsulation
        self._serial = serial
        self._entry_hour = entry_hour
        self._hour_rate = hour_rate
        self._exit_hour = 0
        self._total_cost = 0.0

    def register_exit(self, exit_hour):
        """Registers the exit time of the bicycle."""
        self._exit_hour = exit_hour

    def calculate_cost(self, exit_hour):
        """
        Calculates the service cost based on time spent.
        Validation: Exit hour must be greater than entry hour.
        """
        if exit_hour > self._entry_hour:
            duration = exit_hour - self._entry_hour
            self._total_cost = duration * self._hour_rate
            return self._total_cost
        return -1  # Error indicator for invalid time

    def get_serial(self):
        """Public method to access the private serial attribute."""
        return self._serial


"""
CLASS: App
Description: Main application class that handles the Graphical User Interface.
Inherits from ttk.Window to use Bootstrap styling.
"""


class App(ttk.Window):
    def __init__(self):
        # 1) Initialize the parents class (ttk.Window) with a theme
        super().__init__(themename="flatly")

        # 2) Window configuration
        self.title("Bicycle Workshop Control System")
        self.geometry("600x650")  # A bit taller to show everything

        # 3) Instance of the logic class
        self.auth_system = User()

        # 4) Internal list to store BicycleWorkshop objects
        self.bicycle_list = []

        # 5) Starting the UI components
        self._setup_login_ui()

    def _setup_login_ui(self):
        """Creates the UI elements for the login screen."""
        self.login_frame = ttk.Frame(self, padding=20)
        self.login_frame.pack(expand=True)

        self.title_label = ttk.Label(
            self.login_frame,
            text="Bicycle Workshop Login",
            font=("Helvetica", 18, "bold"),
            bootstyle="primary"
        )
        self.title_label.pack(pady=(0, 20))

        ttk.Label(self.login_frame, text="username:").pack(anchor="w")
        self.username_entry = ttk.Entry(self.login_frame, width=30)
        self.username_entry.pack(pady=(5, 15))

        ttk.Label(self.login_frame, text="password:").pack(anchor="w")
        self.password_entry = ttk.Entry(self.login_frame, width=30, show="*")
        self.password_entry.pack(pady=(5, 20))

        self.login_button = ttk.Button(
            self.login_frame,
            text="Login",
            bootstyle="success",
            command=self._handle_login,
            width=20
        )
        self.login_button.pack(pady=10)

    def _handle_login(self):
        """Validates credentials and transitions to the workshop UI."""
        entered_user = self.username_entry.get()
        entered_pass = self.password_entry.get()

        if self.auth_system.validate_credentials(entered_user, entered_pass):
            messagebox.showinfo("Access Granted", f"Welcome, {entered_user}!")
            self.login_frame.destroy()
            self._setup_workshop_ui()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def _setup_workshop_ui(self):
        """Creates the main workshop management interface."""
        self.workshop_frame = ttk.Frame(self, padding=20)
        self.workshop_frame.pack(expand=True, fill=BOTH)

        ttk.Label(self.workshop_frame, text="Bicycle Registration",
                  font=("Helvetica", 16, "bold"), bootstyle="primary").pack(pady=10)

        # Input section
        input_container = ttk.Frame(self.workshop_frame)
        input_container.pack(pady=10, fill=X)

        ttk.Label(input_container, text="Serial Number:").grid(
            row=0, column=0, padx=5, sticky="W")
        self.serial_entry = ttk.Entry(input_container)
        self.serial_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_container, text="Entry Hour (24H):").grid(
            row=1, column=0, padx=5, sticky="W")
        self.entry_hour_entry = ttk.Entry(input_container)
        self.entry_hour_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_container, text="Price per Hour:").grid(
            row=2, column=0, padx=5, sticky="W")
        self.price_entry = ttk.Entry(input_container)
        self.price_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(
            self.workshop_frame, text="Register Bicycle", bootstyle="success", command=self._register_bicycle)
        self.add_button.pack(pady=10)

        # TABLE AND EXIT SECTION
        ttk.Label(self.workshop_frame, text="Registered Bicycles",
                  font=("Helvetica", 12, "bold")).pack(pady=(10, 5))

        cols = ("Serial", "Status")
        self.bike_table = ttk.Treeview(
            self.workshop_frame, columns=cols, show="headings", height=5)
        for col in cols:
            self.bike_table.heading(col, text=col)
        self.bike_table.pack(pady=5, fill=X)

        # Exit hour section
        exit_container = ttk.Frame(self.workshop_frame)
        exit_container.pack(pady=10, fill=X)

        ttk.Label(exit_container, text="Exit Hour (24H):").grid(
            row=0, column=0, padx=5)
        self.exit_hour_entry = ttk.Entry(exit_container, width=10)
        self.exit_hour_entry.grid(row=0, column=1, padx=5)

        self.exit_button = ttk.Button(
            exit_container, text="Process Exit & Cost", bootstyle="danger", command=self._handle_exit)
        self.exit_button.grid(row=0, column=2, padx=10)

    # BEHAVIOR METHODS

    def _register_bicycle(self):
        """Retrieves data, creates a BicycleWorkshop object, and updates the table."""
        serial = self.serial_entry.get()
        entry_h = self.entry_hour_entry.get()
        price = self.price_entry.get()

        if not serial or not entry_h or not price:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return

        # Check for duplicate serials to prevent logic errors later
        for bike in self.bicycle_list:
            if str(bike.get_serial()) == serial:
                messagebox.showerror(
                    "Error", f"Serial '{serial}' is already registered.")
                return

        try:
            # POO: Instance creation
            new_bike = BicycleWorkshop(serial, float(entry_h), float(price))
            self.bicycle_list.append(new_bike)
            self._update_table()

            # Clear input fields
            self.serial_entry.delete(0, END)
            self.entry_hour_entry.delete(0, END)
            self.price_entry.delete(0, END)
        except ValueError:
            messagebox.showerror(
                "Input Error", "Hours and Price must be numeric.")

    def _update_table(self):
        """Refreshes the Treeview with current list data."""
        for item in self.bike_table.get_children():
            self.bike_table.delete(item)
        for bike in self.bicycle_list:
            self.bike_table.insert("", END, values=(
                bike.get_serial(), "In Workshop"))

    def _handle_exit(self):
        """Processes the cost for the selected bicycle in the table."""
        selected = self.bike_table.selection()
        if not selected:
            messagebox.showwarning(
                "No Selection", "Please select a bicycle from the table.")
            return

        exit_h = self.exit_hour_entry.get()
        if not exit_h:
            messagebox.showwarning(
                "Input Required", "Please enter the exit hour.")
            return

        try:
            item = self.bike_table.item(selected)
            serial = item['values'][0]

            for bike in self.bicycle_list:
                if str(bike.get_serial()) == str(serial):
                    cost = bike.calculate_cost(float(exit_h))
                    if cost == -1:
                        messagebox.showerror(
                            "Time Error", "Exit hour must be greater than entry hour.")
                    else:
                        messagebox.showinfo(
                            "Receipt", f"Bicycle: {serial}\nTotal Cost: ${cost:,.2f}")
                        self.bicycle_list.remove(bike)
                        self._update_table()
                    break
        except ValueError:
            messagebox.showerror("Input Error", "Exit hour must be a number.")

# MAIN EXECUTION BLOCK


if __name__ == "__main__":
    app = App()
    app.mainloop()
