import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import datetime


class ToDoList(ttk.Frame):
    def __init__(self, master):
        self.master = master

        # create to-do list object
        self.tasks = []
        self.date = datetime.date.today().strftime("%Y-%m-%d")

        # create right frames
        self.right_frame = tk.Frame(master, width=200)
        self.top_frame = tk.Frame(self.right_frame, width=200)
        self.top_frame.pack(side=tk.TOP, padx=10, pady=10, fill=tk.NONE)

        # create a Calendar widget and add it to the top_frame
        self.calendar = Calendar(self.top_frame, selectmode="day", date_pattern="yyyy-mm-dd")
        self.calendar.pack(padx=10, pady=10)

        # create entry and button for adding tasks
        self.task_entry = tk.Entry(self.top_frame, width=30)
        self.task_entry.pack(side=tk.LEFT, padx=10)
        self.add_button = tk.Button(self.top_frame, text="Add", command=self.add_task)
        self.add_button.pack(side=tk.LEFT)

        # pack right frames
        self.right_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # create listbox for tasks
        self.task_listbox = tk.Listbox(self.right_frame, width=40)
        self.task_listbox.pack(pady=10)


        # create button for checking tasks
        self.done_button = tk.Button(self.right_frame, text="Done", command=self.done_task)
        self.done_button.pack(side=tk.LEFT, padx=10)


        
        # create button for removing tasks
        self.remove_button = tk.Button(self.right_frame, text="Remove", command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, padx=10)

        # bind the remove button to the task_listbox
        self.task_listbox.bind("<<ListboxSelect>>", self.toggle_remove_button)

        # bind the set_date method to the <<CalendarSelected>> event
        self.calendar.bind("<<CalendarSelected>>", self.set_date)

        # populate task listbox with saved tasks
        self.load_tasks()
        self.update_task_listbox()

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as f:
                tasks = f.read().splitlines()
            for task in tasks:
                self.tasks.append(task)
                self.task_listbox.insert(tk.END, task)
        except FileNotFoundError:
            pass

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append((self.date, task))
            self.task_entry.delete(0, tk.END)
            self.update_task_listbox()


    def toggle_remove_button(self, event):
        # show the done and remove button only when a task is selected
        if self.task_listbox.curselection():
            #self.done_button.pack_forget()
            self.remove_button.pack_forget()
            #self.done_button.pack(side=tk.LEFT, padx=10)
            self.remove_button.pack(side=tk.LEFT, padx=10)
        else:
           # self.done_button.pack_forget()
            self.remove_button.pack_forget()




    def done_task(self):
        index = self.task_listbox.curselection()
        if index:
            # Get the selected task
            task = self.task_listbox.get(index)

            # Check if the task is already done
            fg_color, bg_color = self.task_listbox.itemcget(index, "fg"), self.task_listbox.itemcget(index, "bg")
            if fg_color == "white" and bg_color == "#518a58":
                # If the task is already done, uncheck it
                self.task_listbox.itemconfigure(index, fg="black", bg="white")
                # Update the task data in the tasks list
                for i, t in enumerate(self.tasks):
                    if t[0] == self.date and t[1] == task:
                        self.tasks[i] = (self.date, task, False)
                        break
            else:
                # If the task is not checked, mark it as done
                self.task_listbox.itemconfigure(index, fg="white", bg="#518a58")
                # Update the task data in the tasks list
                for i, t in enumerate(self.tasks):
                    if t[0] == self.date and t[1] == task:
                        self.tasks[i] = (self.date, task, True)
                        break

            # Hide the Done button and show the Remove button
            self.toggle_remove_button(None)
    
                    

    def remove_task(self):
        tasks = self.task_listbox.curselection()
        for task in tasks:
            self.tasks.remove((self.date, self.task_listbox.get(task)))
        self.update_task_listbox()
        self.remove_button.pack_forget()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            if task[0] == self.date:
                task_text = task[1]
                checked = task[2] if len(task) > 2 else False
                fg_color = "white" if checked else "black"
                bg_color = "#518a58" if checked else "white"
                self.task_listbox.insert(tk.END, task_text)
                self.task_listbox.itemconfigure(tk.END, fg=fg_color, bg=bg_color)

        self.toggle_remove_button(None) 
        
        # Call toggle_remove_button to show/hide Remove Task button



    def set_date(self, event=None):
        self.date = self.calendar.selection_get().strftime("%Y-%m-%d")
        self.update_task_listbox()


# root = tk.Tk()
# app = ToDoList(root)
# root.mainloop()