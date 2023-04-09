import tkinter as tk
import time
import configparser

class PomodoroTimer:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.work_time = int(self.config.get('settings', 'work_time', fallback='25')) * 60
        self.break_time = int(self.config.get('settings', 'break_time', fallback='5')) * 60
        self.time_left = self.work_time
        self.is_break = False
        self.is_running = False

        self.root = tk.Tk()
        self.root.title("Pomodoro Timer")

        # create labels
        self.time_label = tk.Label(self.root, text=self.get_time_string(self.time_left), font=("Helvetica", 48))
        self.time_label.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Work", font=("Helvetica", 24))
        self.status_label.pack()

        # create buttons
        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", padx=10)

        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset_timer)
        self.reset_button.pack(side="left", padx=10)

        self.settings_button = tk.Button(self.root, text="Settings", command=self.open_settings)
        self.settings_button.pack(side="right", padx=10)

        self.root.mainloop()

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.update_timer()

    def stop_timer(self):
        self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.is_break = False
        self.time_left = self.work_time
        self.update_time_label()
        self.status_label.config(text="Work")

    def update_timer(self):
        if self.is_running:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_time_label()
                self.root.after(1000, self.update_timer)
            else:
                self.is_running = False
                if not self.is_break:
                    self.time_left = self.break_time
                    self.is_break = True
                    self.status_label.config(text="Break")
                else:
                    self.time_left = self.work_time
                    self.is_break = False
                    self.status_label.config(text="Work")
                self.update_timer()

    def update_time_label(self):
        self.time_label.config(text=self.get_time_string(self.time_left))

    def get_time_string(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")

        work_label = tk.Label(settings_window, text="Work Interval (minutes)")
        work_label.pack()

        work_entry = tk.Entry(settings_window, width=5)
        work_entry.insert(0, int(self.config.get('settings', 'work_time', fallback='25')))
        work_entry.pack()

        break_label = tk.Label(settings_window, text="Break Interval (minutes)")
        break_label.pack()

        break_entry = tk.Entry(settings_window, width=5)
        break_entry.insert(0, int(self.config.get('settings', 'break_time', fallback='5')))
        break_entry.pack()

        save_button = tk.Button(settings_window, text="Save", command=lambda: self.save_settings(settings_window, work_entry.get(), break_entry.get()))
        save_button.pack(pady=10)

    def save_settings(self, settings_window, work_time, break_time):
        self.config.set('settings', 'work_time', work_time)
        self.config.set('settings', 'break_time', break_time)
        with open('config.ini', 'w') as config_file:
            self.config.write(config_file)
        settings_window.destroy()
        self.work_time = int(work_time) * 60
        self.break_time = int(break_time) * 60
        self.time_left = self.work_time
        self.reset_timer()
