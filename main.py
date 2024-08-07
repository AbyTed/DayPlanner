import tkinter as tk
from tkinter import messagebox
from database import ActivitySchedule, session
from functools import partial
from Utils import day_planner


class DayPlannerApp:
    def __init__(self, root):
        self._root = root
        self._root.title("Day Planner")
        self._activities = dict()

        # Labels
        tk.Label(root, text="Activity Name:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(root, text="Difficulty (e/m/h):").grid(
            row=1, column=0, padx=10, pady=5
        )
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
        tk.Button(root, text="Add Activity", command=self.add_activity).grid(
            row=4, column=0, columnspan=2, pady=10
        )
        tk.Button(root, text="Delete Activity", command=self.delete_activity).grid(
            row=5, column=0, columnspan=2, pady=10
        )
        tk.Button(root, text="Submit Activities", command=self.submit_activities).grid(
            row=6, column=0, columnspan=2, pady=10
        )
        tk.Button(root, text="Load Activities", command=self.load_activities).grid(
            row=7, column=0, columnspan=2, pady=10
        )

        # Activity listbox
        self.activity_listbox = tk.Listbox(root, width=50)
        self.activity_listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

        # Schedule display label
        self.schedule_label = tk.Label(root, text="", wraplength=400, justify="left")
        self.schedule_label.grid(row=9, column=0, columnspan=2, padx=10, pady=5)

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
                messagebox.showwarning(
                    "Invalid Time", "Time and break time should be positive integers."
                )
                return
        except ValueError:
            messagebox.showwarning(
                "Invalid Time", "Time and break time should be positive integers."
            )
            return

        if difficulty not in ["e", "m", "h"]:
            messagebox.showwarning(
                "Invalid Difficulty", "Difficulty must be 'e', 'm', or 'h'."
            )
            return

        # Store activity in dictionary
        self._activities[name] = (difficulty, time, break_time)

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
            activity_name = self.activity_listbox.get(index).split(" - ")[0]
            self.activity_listbox.delete(index)
            if activity_name in self._activities:
                del self._activities[activity_name]
        else:
            messagebox.showwarning(
                "No Activity Selected", "Please select an activity to delete."
            )

    def submit_activities(self):
        if not self._activities:
            messagebox.showwarning(
                "No Activities", "Please add activities before submitting."
            )
            return

        # Save activities to database
        for name, (difficulty, time, break_time) in day_planner(
            self._activities
        ).items():

            new_data = ActivitySchedule(
                name=name, difficulty=difficulty, time=time, break_time=break_time
            )
            session.add(new_data)
            session.commit()
        # Clear activities and listbox
        self._activities.clear()
        self.activity_listbox.delete(0, tk.END)

        messagebox.showinfo(
            "Activities Submitted", "Activities have been submitted successfully."
        )

    def load_activities(self):
        # Clear previous schedule display
        self.schedule_label.config(text="")

        try:
            # Load activities from database
            activities = session.query(ActivitySchedule).all()

            # Process activities dictionary

            self.update_schedule_display(activities)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading activities: {str(e)}")

    def update_schedule_display(self, schedule):
        # Clear previous schedule display
        self.schedule_label.config(text="")

        # Display schedule in schedule_label
        if schedule:
            schedule_text = ""
            for activity in schedule:
                activity_info = f"{activity.name} - Difficulty: {activity.difficulty}, Time: {activity.time} mins, Break: {activity.break_time} mins\n"
                schedule_text += activity_info
            self.schedule_label.config(text=schedule_text)
        else:
            self.schedule_label.config(text="No activities added yet.")


if __name__ == "__main__":
    root = tk.Tk()
    app = DayPlannerApp(root)
    root.mainloop()
