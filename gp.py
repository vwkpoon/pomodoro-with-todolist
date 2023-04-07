import time
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage
import math

class PomodoroTimer:

    def __init__ (self):
        self.root = tk.Tk()
        self.root.geometry("600x300")
        self.root.title("Pomodoro Timer")
        self.root.config(padx=100, pady=20, bg="#BA4949")#dark red
        self.root.call('wm', 'iconphoto', self.root._w, PhotoImage(file="tomato.png"))
        
        

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu",16))
        self.s.configure("TButton", font=("Ubuntu",16))

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both",pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab2 = ttk.Frame(self.tabs, width=600, height=100)
        self.tab3 = ttk.Frame(self.tabs, width=600, height=100)

        self.pomodoro_timer_label = tk.Label(self.tab1, text="25:00", font=("Ubuntu", 48))
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = tk.Label(self.tab2, text="05:00", font=("Ubuntu", 48))
        self.short_break_timer_label.pack(pady=20)
        

        self.long_break_timer_label = tk.Label(self.tab3, text="15:00", font=("Ubuntu", 48))
        self.long_break_timer_label.pack(pady=20)
                                              
        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Break")
        self.tabs.add(self.tab3, text="Long Break")

        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=10)
        self.start_button = ttk.Button(self.grid_layout, text = "Start", command=self.start_timer_thread)
        self.start_button.grid(row=0,column =0)

        self.skip_button = ttk.Button(self.grid_layout, text = "Skip", command=self.skip_clock)
        self.skip_button.grid(row=0,column =1)

        self.reset_button = ttk.Button(self.grid_layout, text = "Reset", command=self.reset_clock)
        self.reset_button.grid(row=0,column =2)

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0",font=("Ubuntu", 16))
        self.pomodoro_counter_label.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.pomodoros = 0
        self.skipped = False
        self.stopped = False
        self.running = False
        self.paused = False

        self.root.mainloop()
#clicks the "Pause" button, \n
# they can set a flag to indicate that the timer should pause and stop updating. 
    def start_timer_thread(self):
        if self.running:
            self.paused = not self.paused
            if self.paused:
                self.start_button.config(text="Resume") 
            else:
                self.start_button.config(text="Pause")
                self.resume_timer()               
                  
        else:
            t = threading.Thread(target= self.start_timer)
            t.start()
            self.running = True
            self.start_button.config(text="Pause")
        
    #start timer function
    def start_timer(self):
        self.stopped = False
        self.skipped = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        
        if timer_id == 1:
            self.root.config(padx=100, pady=20, bg="#BA4949")#dark red
            full_seconds = 60* 25
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.pomodoro_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.pomodoros += 1
                self.pomodoro_counter_label.config(text=f"Pomodoros: {self.pomodoros}")
                #function to handle the long break after completing four working pomodoros
                if self.pomodoros % 4 ==0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
                self.start_timer() 
        #short break
        elif timer_id == 2:
            self.root.config(padx=100, pady=20, bg="#38858a") #dark blue
            full_seconds = 60 * 5
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod (full_seconds, 60)
                self.short_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            #if the loop was not stopped again; after a short break, go to pomodoro     
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        #long_break
        elif timer_id == 3: 
            self.root.config(padx=100, pady=20, bg="#518a58") #dark green
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                minutes, seconds = divmod(full_seconds, 60)
                self.long_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
                time.sleep(1)
                full_seconds -= 1
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()  
        else:
            print("Invalid timer id")

    def resume_timer(self):
        t = threading.Thread(target=self.start_timer)
        t.start()
        self.running = True
        self.paused = False
        self.start_button.config(text="Pause")

    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoro = 0 
        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.running = False

    def skip_clock(self):
        current_tab = self.tabs.index(self.tabs.select())
        if current_tab == 0 :
            self.pomodoro_timer_label.config(text="25:00")
        elif current_tab == 1:
            self.short_break_timer_label.config(text="05:00")
        elif current_tab == 2:
            self.long_break_timer_label.config(text="15:00") 
            
        self.stopped = True
        self.skipped = True

PomodoroTimer()

