import customtkinter as ctk
import tkinter as tk

class NetworkInfo(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.lbl_text = tk.StringVar(value='''Basic Network Information''')
        self.detail_level = tk.StringVar(value='Basic')

        self.Label1 = ctk.CTkLabel(self,text='''Network Information''', font=("Roboto Medium", 20))
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

        self.Label4 = ctk.CTkLabel(self.Frame2, text='''Basic Network Information''', font=("Roboto Medium", 11))
        self.Label4.place(relx=0.235, rely=0.01, height=22, width=354)
        self.Label4.configure(textvariable=self.lbl_text)

        self.Text1 = tk.Listbox(self.Frame2)
        self.Text1.place(relx=0.0, rely=0.062, relheight=0.938, relwidth=1.0)

        self.Button1 = ctk.CTkButton(self, text='''Save To File''', font=("Roboto Medium", 11))
        self.Button1.place(relx=0.16, rely=0.94, height=27, relwidth=0.68)
        self.Button1.configure(command=self.on_btn_save_info, fg_color='green', text_color='white')


    def on_btn_save_info(self):
        print(f'networkinfo_support: {self.Text1.get(0, tk.END)}')

    def on_radiobtn_lvl(self):
        print('networkinfo_support.on_radiobtn_lvl')
