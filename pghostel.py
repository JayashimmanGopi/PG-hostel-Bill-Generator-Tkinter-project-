import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class RoomChoice:
    def __init__(self, gender, occupancy, base_cost_per_head):
        self.gender = gender
        self.occupancy = occupancy
        self.base_cost_per_head = base_cost_per_head

    def assign_cost(self, food_option=None, ac_option=None, cleaning_option=None, washing_machine_option=None):
        total_cost_per_head = self.base_cost_per_head

        if food_option == "veg":
            total_cost_per_head=total_cost_per_head+3000
        elif food_option == "nonveg":
            total_cost_per_head=total_cost_per_head+4000

        if ac_option == "yes":
            total_cost_per_head=total_cost_per_head+3000

        if cleaning_option == "yes":
            total_cost_per_head=total_cost_per_head+600

        if washing_machine_option == "yes":
            total_cost_per_head=total_cost_per_head+750

        return total_cost_per_head

class AssignValue:
    def __init__(self):
        self.rooms = {
            "one": RoomChoice(gender="male", occupancy=1, base_cost_per_head=15000),
            "two": RoomChoice(gender="male", occupancy=2, base_cost_per_head=10000),
            "four": RoomChoice(gender="male", occupancy=4, base_cost_per_head=7500),
            "six": RoomChoice(gender="male", occupancy=6, base_cost_per_head=6000)
        }

    def book_room(self, room_type, food_option=None, ac_option=None, cleaning_option=None, washing_machine_option=None, start_date=None, end_date=None):
        room = self.rooms.get(room_type)
        if not room:
            raise ValueError("Invalid room type selected.")

        cost_per_head = room.assign_cost(food_option, ac_option, cleaning_option, washing_machine_option)

        if start_date and end_date:
            try:
                start_date_obj = datetime.strptime(start_date, "%d/%m/%Y")
                end_date_obj = datetime.strptime(end_date, "%d/%m/%Y")
                number_of_days = (end_date_obj - start_date_obj).days
                if number_of_days <= 0:
                    raise ValueError("End date must be after start date.")
                number_of_months = number_of_days // 30  # Approximating the number of months
            except ValueError as e:
                raise ValueError(f"Invalid date format or error in date calculation: {e}")
        else:
            number_of_months = 1

        total_cost = cost_per_head * number_of_months

        return {
            "room_type": room_type,
            "occupancy": room.occupancy,
            "cost_per_head": cost_per_head,
            "total_cost": total_cost,
            "months_stayed": number_of_months
        }

def submit_booking():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    gender = gender_var.get().lower()
    room_type = room_var.get().lower()
    food_option = food_var.get().lower()
    ac_option = ac_var.get().lower()
    cleaning_option = cleaning_var.get().lower()
    washing_machine_option = washing_var.get().lower()
    start_date = entry_start.get().strip()
    end_date = entry_end.get().strip()

    if gender == "female":
        messagebox.showerror("Error", "This is a men's PG hostel.")
        return

    if not name or not age or not room_type or not start_date or not end_date:
        messagebox.showerror("Error", "Please fill all fields.")
        return

    try:
        age = int(age)
        if not (17 < age < 50):
            messagebox.showerror("Error", "Age must be between 17 to 50.")
            return
    except ValueError:
        messagebox.showerror("Error", "Invalid age entered.")
        return

    try:
        booking_details = pg_house.book_room(room_type, food_option, ac_option, cleaning_option, washing_machine_option, start_date, end_date)
        messagebox.showinfo("Booking Details", f"Name: {name}\nAge: {age}\nStart Date: {start_date}\nEnd Date: {end_date}\n"
                            f"Room Type: {booking_details['room_type']}\nOccupancy: {booking_details['occupancy']}\n"
                            f"Cost per Head (per month): {booking_details['cost_per_head']}\n"
                            f"Months Stayed: {booking_details['months_stayed']}\nTotal Cost: {booking_details['total_cost']}")
    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Initialize the PG house data
pg_house = AssignValue()

# Create the main window
root = tk.Tk()
root.title("Heiwa Men's PG-Hostel Booking")

# Set background color
root.configure(bg='#F4A460')

# Center window on screen
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

position_top = int(screen_height / 2 - window_height / 2)
position_right = int(screen_width / 2 - window_width / 2)

root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

# Define the variables for the form
gender_var = tk.StringVar(value="male")
room_var = tk.StringVar(value="one")
food_var = tk.StringVar(value="none")
ac_var = tk.StringVar(value="no")
cleaning_var = tk.StringVar(value="no")
washing_var = tk.StringVar(value="no")

# Create form elements in the center with padding
tk.Label(root, text="Name:", bg='#F4A460').grid(row=0, column=0, pady=20, padx=25)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, pady=20, padx=25)

tk.Label(root, text="Age (Age must be 17 to 50):", bg='#F4A460').grid(row=1, column=0, pady=20, padx=25)
entry_age = tk.Entry(root)
entry_age.grid(row=1, column=1, pady=20, padx=25)

tk.Label(root, text="Gender:", bg='#F4A460').grid(row=2, column=0, pady=20, padx=25)
tk.Radiobutton(root, text="Male", variable=gender_var, value="male", bg='#F4A460').grid(row=2, column=1, pady=20, padx=25)

tk.Label(root, text="Room Type:", bg='#F4A460').grid(row=3, column=0, pady=20, padx=25)
tk.Radiobutton(root, text="Single", variable=room_var, value="one", bg='#F4A460').grid(row=3, column=1, pady=20, padx=25)
tk.Radiobutton(root, text="Double", variable=room_var, value="two", bg='#F4A460').grid(row=3, column=2, pady=20, padx=25)
tk.Radiobutton(root, text="Four Sharing", variable=room_var, value="four", bg='#F4A460').grid(row=3, column=3, pady=20, padx=25)
tk.Radiobutton(root, text="Six Sharing", variable=room_var, value="six", bg='#F4A460').grid(row=3, column=4, pady=20, padx=25)

tk.Label(root, text="Food Option:", bg='#F4A460').grid(row=4, column=0, pady=5, padx=10)
tk.Radiobutton(root, text="Veg", variable=food_var, value="veg", bg='#F4A460').grid(row=4, column=1, pady=20, padx=25)
tk.Radiobutton(root, text="Non-Veg", variable=food_var, value="nonveg", bg='#F4A460').grid(row=4, column=2, pady=20, padx=25)
tk.Radiobutton(root, text="None", variable=food_var, value="none", bg='#F4A460').grid(row=4, column=3, pady=20, padx=25)

tk.Label(root, text="AC Option:", bg='#F4A460').grid(row=5, column=0, pady=20, padx=25)
tk.Radiobutton(root, text="Yes", variable=ac_var, value="yes", bg='#F4A460').grid(row=5, column=1, pady=20, padx=25)
tk.Radiobutton(root, text="No", variable=ac_var, value="no", bg='#F4A460').grid(row=5, column=2, pady=20, padx=25)

tk.Label(root, text="Cleaning Option:", bg='#F4A460').grid(row=6, column=0, pady=20, padx=25)
tk.Radiobutton(root, text="Yes", variable=cleaning_var, value="yes", bg='#F4A460').grid(row=6, column=1, pady=20, padx=25)
tk.Radiobutton(root, text="No", variable=cleaning_var, value="no", bg='#F4A460').grid(row=6, column=2, pady=20, padx=25)

tk.Label(root, text="Washing Machine Option:", bg='#F4A460').grid(row=7, column=0, pady=20, padx=25)
tk.Radiobutton(root, text="Yes", variable=washing_var, value="yes", bg='#F4A460').grid(row=7, column=1, pady=20, padx=25)
tk.Radiobutton(root, text="No", variable=washing_var, value="no", bg='#F4A460').grid(row=7, column=2, pady=20, padx=25)

tk.Label(root, text="Start Date (DD/MM/YYYY):", bg='#F4A460').grid(row=8, column=0, pady=20, padx=25)
entry_start = tk.Entry(root)
entry_start.grid(row=8, column=1, pady=20, padx=25)

tk.Label(root, text="End Date (DD/MM/YYYY):", bg='#F4A460').grid(row=9, column=0, pady=20, padx=25)
entry_end = tk.Entry(root)
entry_end.grid(row=9, column=1, pady=20, padx=25)

# Submit button
tk.Button(root, text="Submit Booking", command=submit_booking).grid(row=10, column=0, columnspan=20, pady=15)

# Run the application
root.mainloop()
