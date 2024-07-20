import tkinter as tk
from tkinter import messagebox
from Utils import day_planner, display_schedule

class DayPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Day Planner")

        self.activities = {}

        # Labels
        tk.Label(root, text="Activity Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Difficulty (e/m/h):").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(root, text="Time (mins):").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(root, text="Break Time (mins):").grid(row=3, column=0, padx=10, pady=5)

        # Entry fields
        self.activity_name_entry = tk.Entry(root, width=30)
        self.activity_name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.difficulty_entry = tk.Entry(root, width=30)
        self.difficulty_entry.grid(row=1, column=1, padx=10, pady=5)

        self.time_entry = tk.Entry(root, width=30)
        self.time_entry.grid(row=2, column=1, padx=10, pady=5)

        self.break_time_entry = tk.Entry(root, width=30)
        self.break_time_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(root, text="Add Activity", command=self.add_activity).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Delete Activity", command=self.delete_activity).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(root, text="Submit Activities", command=self.submit_activities).grid(row=6, column=0, columnspan=2, pady=10)

        # Activity listbox
        self.activity_listbox = tk.Listbox(root, width=50)
        self.activity_listbox.grid(row=7, column=0, columnspan=2, padx=10, pady=5)

        # Schedule frame
        self.schedule_frame = tk.Frame(root, bg="white", bd=2, relief=tk.SUNKEN)
        self.schedule_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def add_activity(self):
        name = self.activity_name_entry.get().strip()
        difficulty = self.difficulty_entry.get().strip().lower()
        time_str = self.time_entry.get().strip()
        break_time_str = self.break_time_entry.get().strip()

        # Validate inputs
        if not name or not difficulty or not time_str or not break_time_str:
            messagebox.showwarning("Incomplete Input", "Please fill out all fields.")
            return

        try:
            time = int(time_str)
            break_time = int(break_time_str)
            if time <= 0 or break_time < 0:
                messagebox.showwarning("Invalid Time", "Time and break time should be positive integers.")
                return
        except ValueError:
            messagebox.showwarning("Invalid Time", "Time and break time should be positive integers.")
            return

        if difficulty not in ['e', 'm', 'h']:
            messagebox.showwarning("Invalid Difficulty", "Difficulty must be 'e', 'm', or 'h'.")
            return

        # Store activity in dictionary
        self.activities[name] = (time, difficulty, break_time)

        # Update listbox display
        activity_info = f"{name} - Difficulty: {difficulty}, Time: {time} mins, Break: {break_time} mins"
        self.activity_listbox.insert(tk.END, activity_info)

        # Clear entry fields
        self.activity_name_entry.delete(0, tk.END)
        self.difficulty_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.break_time_entry.delete(0, tk.END)

    def delete_activity(self):
        selected_index = self.activity_listbox.curselection()
        if selected_index:
            index = selected_index[0]
            activity_name = self.activity_listbox.get(index).split(' - ')[0]
            self.activity_listbox.delete(index)
            if activity_name in self.activities:
                del self.activities[activity_name]
        else:
            messagebox.showwarning("No Activity Selected", "Please select an activity to delete.")

    def submit_activities(self):
        if not self.activities:
            messagebox.showwarning("No Activities", "Please add activities before submitting.")
            return

        
        # Process activities dictionary
        ordered_schedule = day_planner(self.activities)

        # Display schedule
        self.update_schedule_display(ordered_schedule)

        # Clear activities and listbox
        self.activities.clear()
        self.activity_listbox.delete(0, tk.END)

        messagebox.showinfo("Activities Submitted", "Activities have been submitted successfully.")

       

    def update_schedule_display(self, schedule):
        # Clear previous schedule display
        for widget in self.schedule_frame.winfo_children():
            widget.destroy()

        # Display schedule in schedule_frame
        if schedule:
            row = 0
            for activity, (time, difficulty, break_time) in schedule.items():
                # Display activity
                activity_label = tk.Label(self.schedule_frame, text=f"{activity} | Time: {time} mins | Difficulty: {difficulty.upper()}", anchor="w", justify="left", bg="white", padx=10, pady=5)
                activity_label.grid(row=row, column=0, sticky="w")

                # Display break time
                break_label = tk.Label(self.schedule_frame, text=f"Break | Time: {break_time} mins", anchor="w", justify="left", bg="lightgray", padx=10, pady=5)
                break_label.grid(row=row + 1, column=0, sticky="w")

                row += 2  # Move to the next row for the next activity

        else:
            tk.Label(self.schedule_frame, text="No activities added yet.", bg="white").grid(row=0, column=0, sticky="w", padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = DayPlannerApp(root)
    root.mainloop()
