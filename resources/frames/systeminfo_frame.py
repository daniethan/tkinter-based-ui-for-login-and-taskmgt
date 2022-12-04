import customtkinter as ctk, time
import tkinter as tk
import config.vars_ as vars_
from tkinter import simpledialog, messagebox
from resources.services.appfuncs import (
    get_sys_info
)
from resources.services.auth import auth_with_pin

class SystemInfo(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.basic_data = [
            'memory', 'bios', 'host', 'processor', 'os name', 'card', 
        ]
        self.lbl_text = tk.StringVar(value='''Basic''')
        self.detail_level = tk.StringVar(value='Basic')

        self.Label1 = ctk.CTkLabel(self,text='''System Information''', font=("Roboto Medium", 20))
        self.Label1.place(relx=0.34, rely=0.019)

        self.Frame1 = ctk.CTkFrame(self)
        self.Frame1.place(relx=0.167, rely=0.094, relheight=0.138, relwidth=0.642)

        self.Label2 = ctk.CTkLabel(self.Frame1, text='''Choose level of detail''', font=("Roboto Medium", 11))
        self.Label2.place(relx=0.25, rely=0.05, height=22, width=244)

        self.Radiobutton1 = ctk.CTkRadioButton(self.Frame1, text='''Basic''', value='Basic')
        self.Radiobutton1.place(relx=0.319, rely=0.411, relheight=0.342, relwidth=0.151)
        self.Radiobutton1.configure(command=self.on_radiobtn_lvl, variable=self.detail_level)

        self.Radiobutton1_1 = ctk.CTkRadioButton(self.Frame1, text='''Full''', value='Full')
        self.Radiobutton1_1.place(relx=0.548, rely=0.411, relheight=0.342, relwidth=0.125)
        self.Radiobutton1_1.configure(command=self.on_radiobtn_lvl, variable=self.detail_level)

        self.Frame2 = ctk.CTkFrame(self)
        self.Frame2.place(relx=0.067, rely=0.255, relheight=0.666, relwidth=0.875)

        self.Label4 = ctk.CTkLabel(self.Frame2, text=f"{self.lbl_text.get()} System Information", font=("Roboto Medium", 11))
        self.Label4.place(relx=0.235, rely=0.01, height=22, width=354)

        self.Text1 = tk.Listbox(self.Frame2, font=("Segoui UI", 10))
        self.Text1.place(relx=0.0, rely=0.062, relheight=0.938, relwidth=1.0)

        self.Button1 = ctk.CTkButton(self, text='''Save To File''', font=("Roboto Medium", 11))
        self.Button1.place(relx=0.16, rely=0.94, height=27, relwidth=0.68)
        self.Button1.configure(command=self.on_btn_save_info, fg_color='green', text_color='white')
        
        self._get_sys_info(basic=self.detail_level.get())

    def on_btn_save_info(self):
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
                with open("savedfiles\\file.txt", 'a') as file:
                    file.write(f"{time.ctime(time.time())}\n")
                    for item in self.Text1.get(0, tk.END):
                        file.write(f"{item.strip()}\n")
                    
                    file.write("\n")
                messagebox.showinfo('File Saved', f"System Info was saved successfully!")
                break
            else:
                trials -= 1
                messagebox.showwarning('Incorrect PIN', f"Incorrect Auth PIN!\n{trials} trial(s) remaining.")
        else:
            messagebox.showerror('Incorrect PIN', f"Wrong PIN provided more tham 3 times. Locked out!")
            vars_.APP.home(False)

    def on_radiobtn_lvl(self):
        self._get_sys_info(basic=self.detail_level.get())

    def _get_sys_info(self, basic: str='Basic'):
        self.info = get_sys_info()
        self.Label4.configure(text=f"{basic} System Information")
        self.Text1.delete(0,tk.END)

        if basic == 'Full' and self.info is not None:
            trials = 3
            while trials > 0:
                pin = simpledialog.askinteger(
                    'Auth PIN',
                    "Enter your 5-digit Auth PIN to confirm",
                )
                if pin==0 or pin is None:
                    basic = 'Basic'
                    self.detail_level.set('Basic')
                    break
                is_auth = auth_with_pin(pin=str(pin), trials=(trials > 0))
                if is_auth:
                    messagebox.showinfo('Success', f"Correct Pin\nFull System information is being fetched\nPlease close this box first.")
                    for details in sorted(self.info):
                        if details.split(':')[0][0:3].isalpha():
                            self.Text1.insert(tk.END, f"  {details}")                      
                    break
                else:
                    trials -= 1
                    messagebox.showwarning('Incorrect PIN', f"Incorrect Auth PIN!\n{trials} trial(s) remaining.")
            else:
                messagebox.showerror('Incorrect PIN', f"Wrong PIN provided more tham 3 times. Locked out!")    
                vars_.APP.home(False)        


        if basic=='Basic' and self.info is not None:
            for details in sorted(self.info):
                if True in [f in details.split(':')[0].lower() for f in self.basic_data]:
                    self.Text1.insert(tk.END, f"  {details}")

