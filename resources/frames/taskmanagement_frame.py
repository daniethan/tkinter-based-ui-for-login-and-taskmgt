import subprocess, os
from config import vars_
import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog,messagebox
from resources.services.auth import auth_with_pin
from resources.services.appfuncs import (
    search,
    get_running_tasks
)

class TaskManager(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        
        self.search_query = tk.StringVar()
        self.search_result = tk.StringVar()
        self.selected_task = tk.StringVar()

        self.Label1 = ctk.CTkLabel(self, font=("Roboto Medium", 20))
        self.Label1.place(relx=0.38, rely=0.019)
        self.Label1.configure(text='''Task Manager''')

        self.Frame1 = ctk.CTkFrame(self)
        self.Frame1.place(relx=0.015, rely=0.084, relheight=0.914, relwidth=0.526)

        self.Entry1 = ctk.CTkEntry(self.Frame1)
        self.Entry1.place(relx=0.017, rely=0.021, height=24, relwidth=0.653)
        self.Entry1.configure(textvariable=self.search_query)

        self.Button2 = ctk.CTkButton(self.Frame1)
        self.Button2.place(relx=0.685, rely=0.021, height=24, relwidth=0.3)
        self.Button2.configure(text='''Search''', font=("Roboto Medium", 11))
        self.Button2.configure(fg_color='dark blue', text_color='white')
        self.Button2.configure(command=self.on_btn_search)

        self.Label3 = ctk.CTkLabel(self.Frame1, font=("Roboto Medium", 11))
        self.Label3.place(relx=0.35, rely=0.065)
        self.Label3.configure(text='''Search Results''', font=("Roboto Medium", 12))

        self.Listbox2 = tk.Listbox(self.Frame1, activestyle='none', font=("Segoui UI", 10))
        self.Listbox2.place(relx=-0.003, rely=0.1, relheight=0.82, relwidth=1.006)
        self.Listbox2.configure(listvariable=self.search_result)

        self.Button2 = ctk.CTkButton(self.Frame1)
        self.Button2.place(relx=0.05, rely=0.945, height=28, relwidth=0.9)
        self.Button2.configure(command=self.on_btn_run, fg_color='green', text_color='white')
        self.Button2.configure(text='''Run the selected Program''', font=("Roboto Medium", 11))

        self.Frame2 = ctk.CTkFrame(self)
        self.Frame2.place(relx=0.557, rely=0.086, relheight=0.91, relwidth=0.429)

        self.Label2 = ctk.CTkLabel(self.Frame2)
        self.Label2.place(relx=0.3, rely=0.012)
        self.Label2.configure(text='''Running Programs''', font=("Roboto Medium", 12))

        self.Listbox1 = tk.Listbox(self.Frame2, activestyle='none', font=("Segoui UI", 10))
        self.Listbox1.place(relx=0.0, rely=0.063, relheight=0.86, relwidth=1.0)
        self.Listbox1.configure(relief="flat")
        self.Listbox1.configure(listvariable=self.selected_task)

        self.Button1 = ctk.CTkButton(self.Frame2)
        self.Button1.place(relx=0.05, rely=0.945, height=28, relwidth=0.9)
        self.Button1.configure(command=self.on_btn_stop, fg_color='green', text_color='white')
        self.Button1.configure(text='''Stop Selected Program''', font=("Roboto", 12))

        self.get_tasks()
        self.on_btn_search()

    
    def on_btn_run(self):
        index = self.Listbox2.curselection()
        if len(index) > 0:
            trials = 3
            while trials > 0:
                pin = simpledialog.askinteger(
                    'Auth PIN',
                    "Enter your 5-digit Auth PIN to confirm",
                )
                if pin==0 or pin is None:
                    break

                is_auth = auth_with_pin(pin=str(pin), trials=(trials > 0))
                if is_auth:
                    messagebox.showinfo('Success', f"Correct PIN\nSelected Program runs after you close this box.")
                    filename = self.Listbox2.get(index).strip()
                    subprocess.run(f'"{os.path.realpath(self.result.get(filename))}"')
                    break
                else:
                    trials -= 1
                    messagebox.showwarning('Incorrect PIN', f"Incorrect Auth PIN!\n{trials} trial(s) remaining.")
            else:
                messagebox.showerror('Incorrect PIN', f"Wrong PIN provided more tham 3 times. Locked out!")
                vars_.APP.home(False)
        else:
            messagebox.showerror('Incorrect Input', f"Please select a program to RUN!")

    def on_btn_search(self):
        self.Listbox2.delete(0, tk.END)
        self.Listbox2.insert(tk.END, f"Searching for {self.search_query.get()}. Please wait...")
        self.result = {file:path for file,path in search(filename=self.search_query.get())}

        if self.result is not None:
            self.Listbox2.delete(0, tk.END)
            for i, f in enumerate(sorted(set(self.result.items())), start=1):
                self.Listbox2.insert(i, f"  {f[0]}")
        else:
            self.Listbox2.delete(0, tk.END)
            self.Listbox2.insert(0, " ")
            self.Listbox2.insert(1, f"  No executable files with name {self.search_query.get()} were found")
            self.Listbox2.configure(state='disabled')

    def on_btn_stop(self):
        ind = self.Listbox1.curselection()
        if len(ind) > 0:
            trials = 3
            while trials > 0:
                pin = simpledialog.askinteger(
                    'Auth PIN',
                    "Enter your 5-digit Auth PIN to confirm",
                )
                if pin==0 or pin is None:
                    break

                is_auth = auth_with_pin(pin=str(pin), trials=(trials > 0))
                if is_auth:
                    messagebox.showinfo('Success', f"Correct PIN\nSelected Program stops after you close this box.")
                    task = self.Listbox1.get(ind)
                    #kill to stop selected task
                    code = subprocess.run(f"taskkill /im {task}",capture_output=True).returncode
                    if not code:
                        self.Listbox1.delete(0,tk.END)
                        self.get_tasks()
                    break
                else:
                    trials -= 1
                    messagebox.showwarning('Incorrect PIN', f"Incorrect Auth PIN!\n{trials} trial(s) remaining.")
            else:
                messagebox.showerror('Incorrect PIN', f"Wrong PIN provided more tham 3 times. Locked out!")
                vars_.APP.home(False)
        else: 
            messagebox.showerror('Incorrect Input', f"Please select a program to terminate!")

    def get_tasks(self):
        tasks = get_running_tasks()
        if tasks is not None:
            self.Listbox1.delete(0,tk.END)
            for taskname in sorted(set(tasks)):
                self.Listbox1.insert(tk.END, f"  {taskname}")

