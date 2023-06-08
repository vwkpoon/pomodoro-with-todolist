import tkinter as tk
from pomodoro_timer import PomodoroTimer
from to_do_with_calendar import ToDoList

import time
#from tkinter import ttk, PhotoImage

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pomodoro Timers")
        self.geometry("800x480")
        

        # Define a handler for the "WM_DELETE_WINDOW" protocol
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create two frames for the timers
        self.timer_frame_left = tk.Frame(self, width=400, height=400)
        self.timer_frame_left.pack(side="left", fill="both", expand=True)

    
        self.to_do_frame = tk.Frame(self, width=400, height=480)
        self.to_do_frame.pack(side="right", fill="both", expand=True)    
        
        
        # Create instances of PomodoroTimer in each frame
        self.pomodoro_timer_left = PomodoroTimer(self.timer_frame_left)
        self.to_do_list = ToDoList(self.to_do_frame)
        
    def on_close(self):
        # Stop the timers and reset the clocks before closing the program
        self.pomodoro_timer_left.reset_clock()
        #self.pomodoro_timer_right.reset_clock()
        # Wait for the timer threads to finish before destroying the root window
        while self.pomodoro_timer_left.running:
            time.sleep(0.1)
        self.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()