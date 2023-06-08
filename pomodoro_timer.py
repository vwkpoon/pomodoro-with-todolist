import time
import threading
import tkinter as tk
from tkinter import ttk
import winsound

class PomodoroTimer(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=("Ubuntu",16))
        self.s.configure("TButton", font=("Ubuntu",16))
        

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="none",pady=20, expand=False)
        self.tabs.pack_propagate(False)

        self.tab1 = tk.Frame(self.tabs, width=600, height=300, bg="#BA4949")
        self.tab2 = tk.Frame(self.tabs, width=600, height=300, bg="#38858a")
        self.tab3 = tk.Frame(self.tabs, width=600, height=300, bg="#518a58")

        self.pomodoro_timer_label = tk.Label(self.tab1, text="25:00", font=("Ubuntu", 48),bg="#BA4949",fg="white")
        self.pomodoro_timer_label.pack(pady=20)

        self.short_break_timer_label = tk.Label(self.tab2, text="05:00", font=("Ubuntu", 48),bg="#38858a",fg="white")
        self.short_break_timer_label.pack(pady=20)

        self.long_break_timer_label = tk.Label(self.tab3, text="15:00", font=("Ubuntu", 48),bg="#518a58",fg="white")
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
        
        #self.root.mainloop()
        # Initialize the music thread variable
        self.music_thread = None
        
    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target= self.start_timer)
            t.start()
            self.running = True
        else:
            self.paused = not self.paused
            if self.paused:
                self.start_button.configure(text="Start")
            else:
                self.start_button.configure(text="Pause")

        
    #start timer function
    def start_timer(self):
        self.stopped = False
        self.skipped = False
        self.paused = False
        timer_id = self.tabs.index(self.tabs.select()) + 1
        self.start_button.configure(text="Pause")
        if timer_id == 1:
            self.root.config(bg="#BA4949")#dark red
            full_seconds = 60*25
            while full_seconds > 0 and not self.stopped:
                if not self.paused:
                    minutes, seconds = divmod(full_seconds, 60)
                    self.pomodoro_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                    self.root.update()
                    time.sleep(1)
                    full_seconds -= 1
                    if full_seconds <=0:
                            self.stop_music()
                    else:
                        if full_seconds <= 2 and not self.music_thread:
                            self.music_thread = threading.Thread(target=self.play_alarm)
                            self.music_thread.start()
                else:
                    time.sleep(0.5)
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
            self.root.config(bg="#38858a") #dark blue
            full_seconds = 60*5
            while full_seconds > 0 and not self.stopped:
                if not self.paused:
                    minutes, seconds = divmod (full_seconds, 60)
                    self.short_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                    #self.root.update()
                    time.sleep(1)
                    full_seconds -= 1
                    if full_seconds <=0:
                            self.stop_music()
                    else:
                        if full_seconds <= 2 and not self.music_thread:
                            self.music_thread = threading.Thread(target=self.play_alarm)
                            self.music_thread.start()
                else:
                    time.sleep(0.5)
            #if the loop was not stopped again; after a short break, go to pomodoro     
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer()
        #long_break
        elif timer_id == 3: 
            self.root.config(bg="#518a58") #dark green
            full_seconds = 60 * 15
            while full_seconds > 0 and not self.stopped:
                if not self.paused:
                    minutes, seconds = divmod(full_seconds, 60)
                    self.long_break_timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
                    #self.root.update()
                    time.sleep(1)
                    full_seconds -= 1
                    if full_seconds <=0:
                            self.stop_music()
                    else:
                        if full_seconds <= 2 and not self.music_thread:
                            self.music_thread = threading.Thread(target=self.play_alarm)
                            self.music_thread.start()
                else:
                    time.sleep(0.1)
            if not self.stopped or self.skipped:
                self.tabs.select(0)
                self.start_timer() 
                
                 
        else:
            print("Invalid timer id")

    def reset_clock(self):
        self.stopped = True
        self.skipped = False
        self.pomodoro = 0 
        self.pomodoro_timer_label.config(text="25:00")
        self.short_break_timer_label.config(text="05:00")
        self.long_break_timer_label.config(text="15:00")
        self.pomodoro_counter_label.config(text="Pomodoros: 0")
        self.root.config(bg="white")# return to white
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
        
    def play_alarm(self):
        # Load and play the built-in sound
        winsound.PlaySound("C:\\Windows\\Media\\tada.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

        # Wait for the sound to finish playing
        time.sleep(5)
        # Stop the sound
        winsound.PlaySound(None, winsound.SND_PURGE)
    def stop_music(self):
        if self.music_thread:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.music_thread.join()
            self.music_thread = None


# # for test only
# root =tk.Tk()
# pomodoro_timer = PomodoroTimer(root) # passing root only once


# root.mainloop()


