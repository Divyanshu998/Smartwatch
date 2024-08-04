import datetime
import time
import tkinter as tk
from tkinter import simpledialog, messagebox

class Exercise:
    def _init_(self, name, description, duration, intensity):
        self.name = name
        self.description = description
        self.duration = duration
        self.intensity = intensity

class User:
    def _init_(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height
        self.workout_log = []

    def bmi(self):
        return self.weight / ((self.height / 100) ** 2)

    def log_workout(self, exercise, date=None, heart_rate=None):
        if date is None:
            date = datetime.date.today()
        self.workout_log.append((date, exercise, heart_rate))

    def get_workout_summary(self):
        return [(date, exercise.name, heart_rate) for date, exercise, heart_rate in self.workout_log]

class StopwatchApp(tk.Toplevel):
    def _init_(self, parent):
        super()._init_(parent)
        self.title("Stopwatch")
        self.geometry("400x250")
        self.running = False
        self.start_time = None
        self.elapsed_time = 0

        self.label = tk.Label(self, text="0.00", font=("Helvetica", 48))
        self.label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start", command=self.start)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.reset_button = tk.Button(self, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=20, pady=10)

        self.heart_rate_label = tk.Label(self, text="Heart Rate (bpm):", font=("Helvetica", 14))
        self.heart_rate_label.pack(pady=5)

        self.heart_rate_entry = tk.Entry(self, font=("Helvetica", 14))
        self.heart_rate_entry.pack(pady=5)

        self.submit_button = tk.Button(self, text="Submit Heart Rate", command=self.submit_heart_rate)
        self.submit_button.pack(pady=10)

        self.heart_rate = None
        self.update_id = None

        # Background color animation
        self.colors = ["#f0f0f0", "#ffcccc", "#ccffcc", "#ccccff", "#ffccff"]
        self.color_index = 0
        self.change_background()

    def start(self):
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.update()
            self.running = True

    def stop(self):
        if self.running:
            self.after_cancel(self.update_id)
            self.elapsed_time = time.time() - self.start_time
            self.running = False

    def reset(self):
        self.stop()
        self.start_time = None
        self.elapsed_time = 0
        self.label.config(text="0.00")

    def update(self):
        self.elapsed_time = time.time() - self.start_time
        self.label.config(text=f"{self.elapsed_time:.2f}")
        self.update_id = self.after(50, self.update)

    def submit_heart_rate(self):
        try:
            heart_rate = int(self.heart_rate_entry.get())
            if heart_rate < 0:
                messagebox.showerror("Invalid Input", "Heart rate cannot be negative.")
            else:
                self.heart_rate = heart_rate
                messagebox.showinfo("Heart Rate", f"Heart rate recorded: {heart_rate} bpm")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def change_background(self):
        self.config(bg=self.colors[self.color_index])
        self.color_index = (self.color_index + 1) % len(self.colors)
        self.after(500, self.change_background)

class SmartwatchApp(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Smartwatch")
        self.geometry("300x200")

        self.user = User("John Doe", 30, 70, 175)
        
        self.label = tk.Label(self, text="Smartwatch App", font=("Helvetica", 18))
        self.label.pack(pady=20)

        self.stopwatch_button = tk.Button(self, text="Start Stopwatch", command=self.open_stopwatch)
        self.stopwatch_button.pack(pady=10)

        self.summary_button = tk.Button(self, text="View Workout Summary", command=self.view_summary)
        self.summary_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

    def open_stopwatch(self):
        self.stopwatch = StopwatchApp(self)
        self.stopwatch.protocol("WM_DELETE_WINDOW", self.on_stopwatch_close)

    def on_stopwatch_close(self):
        if self.stopwatch.heart_rate is not None:
            exercise = Exercise("Generic Exercise", "Recorded with Stopwatch", self.stopwatch.elapsed_time, "Variable")
            self.user.log_workout(exercise, heart_rate=self.stopwatch.heart_rate)
        self.stopwatch.destroy()

    def view_summary(self):
        summary_window = tk.Toplevel(self)
        summary_window.title("Workout Summary")
        summary_window.geometry("400x300")

        summary_label = tk.Label(summary_window, text="Workout Summary", font=("Helvetica", 16))
        summary_label.pack(pady=10)

        for entry in self.user.get_workout_summary():
            date, exercise_name, heart_rate = entry
            entry_label = tk.Label(summary_window, text=f"Date: {date}, Exercise: {exercise_name}, Heart Rate: {heart_rate} bpm")
            entry_label.pack()

if _name_ == "_main_":
    app = SmartwatchApp()
    app.mainloop()
