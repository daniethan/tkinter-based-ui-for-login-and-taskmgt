import customtkinter as ctk
import tkinter as tk
from config import dbconfig, models, vars_
from resources.frames import (
    login_frame,
    systeminfo_frame,
    taskmanagement_frame,
    login_frame
)


models.Base.metadata.create_all(bind=dbconfig.engine)

ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):

    WIDTH = 1080
    HEIGHT = 760
    is_auth: bool = False

    def __init__(self):
        super().__init__()

        self.title("Simple OS function UI")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}+250+50")
        self.resizable(True, False)
        self.attributes('-alpha', 0.98)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(7, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = ctk.CTkLabel(master=self.frame_left,
                                              text="Function Navigator",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        self.button_0 = ctk.CTkButton(master=self.frame_left,
                                                text="Login",
                                                command=self.home_)
        self.button_0.grid(row=2, column=0, pady=10, padx=20)

        self.button_1 = ctk.CTkButton(master=self.frame_left,
                                                text="Manage Tasks",
                                                command=self.manage_tasks)
        self.button_1.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = ctk.CTkButton(master=self.frame_left,
                                                text="System Info",
                                                command=self.get_sysinfo)
        self.button_3.grid(row=5, column=0, pady=10, padx=20)

        self.button_4 = ctk.CTkButton(master=self.frame_left,
                                                text="Back Home",
                                                command=lambda x = True: self.home(x),)
        self.button_4.grid(row=6, column=0, pady=10, padx=20)

        self.label_mode = ctk.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=20, sticky="w")

        self.optionmenu_1 = ctk.CTkOptionMenu(master=self.frame_left,
                                                        values=["Light", "Dark", "System"],
                                                        command=self.change_appearance_mode)
        self.optionmenu_1.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        
        # ============ frame_right ============
        self.frame_right = self.home(is_authenticated=App.is_auth)
        
    def home(self, is_authenticated: bool): 
        self.frame_right = ctk.CTkFrame(master=self, corner_radius=5)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        self._info = ctk.CTkLabel(master=self.frame_right,
                                    text="Welcome to Simple OS function UI\nFeel at home.", 
                                    justify='center', font=("Roboto Medium", 24))

        if not is_authenticated:
            vars_.USER = None
            self.login = login_frame.LoginFrame(master=self.frame_right, home=self.home)
            App.is_auth = is_authenticated
            self.button_0.configure(text = "Login")
            self.login.place(relx=0.10, rely=0.125, relheight=0.75, relwidth=0.80)
        else:
            self.button_0.configure(text="Logout")
            App.is_auth = is_authenticated
            self._info.grid(row=0, column=0, columnspan=2, pady=200, padx=200, sticky="nsew")              
            
            self.Frame1 = ctk.CTkFrame(self.frame_right)
            self.Frame1.place(relx=0.133, rely=0.62, relheight=0.235, relwidth=0.75)

            self.user_lbl = ctk.CTkLabel(self.Frame1)
            self.user_lbl.place(relx=0.01, rely=0.12, relwidth=0.98)
            self.user_lbl.configure(text=f'''Hi!''', font=("Roboto Medium", 16))
            if vars_.USER is not None:
                self.user_lbl.configure(text=f'''Hi, {vars_.USER.name.title()}''', font=("Roboto Medium", 16))
            
            self.Button4 = ctk.CTkButton(self.Frame1)
            self.Button4.place(relx=0.04, rely=0.39, relheight=0.20, relwidth=0.45)
            self.Button4.configure(text='''My Profile''', command=login_frame.send_feature_notice)

            self.Button5 = ctk.CTkButton(self.Frame1)
            self.Button5.place(relx=0.51, rely=0.39, relheight=0.20, relwidth=0.45)
            self.Button5.configure(text='''Update Profile''', command=login_frame.send_feature_notice)

            self.Label4 = ctk.CTkLabel(self.Frame1)
            self.Label4.place(relx=0.01, rely=0.755,relwidth=0.98)
            self.Label4.configure(text='''This App helps you manage tasks (run/stop programs) and also view your computer's details once logged in.''')
        
        if self.button_0._text == 'Login':
            self.button_4.configure(state='disabled')
        else: 
            self.button_4.configure(state='normal')

        return self.frame_right


    def get_sysinfo(self):
        if App.is_auth:
            self.frame_right = systeminfo_frame.SystemInfo(master=self, corner_radius=5)
            self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        else:
            self.frame_right = ctk.CTkFrame(master=self, corner_radius=5)
            self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
            self._info = ctk.CTkLabel(master=self.frame_right,
                                    text="View all your system information\nWith just a click!", 
                                    justify='center', font=("Roboto Medium", 24))
            self._info.grid(row=0, column=0, columnspan=2, pady=200, padx=200, sticky="nsew")
            
            self.Frame1 = ctk.CTkFrame(self.frame_right)
            self.Frame1.place(relx=0.133, rely=0.62, relheight=0.235, relwidth=0.75)

            self.Button4 = ctk.CTkButton(self.Frame1)
            self.Button4.place(relx=0.15, rely=0.60, relheight=0.25, relwidth=0.70)
            self.Button4.configure(text='''Login''', command=self.home_)

            self.Label4 = ctk.CTkLabel(self.Frame1)
            self.Label4.place(relx=0.01, rely=0.20, relheight=0.15, relwidth=0.98)
            self.Label4.configure(text='''Login to view all your system information''')


    def manage_tasks(self):
        self._info.configure(text="""Run/Stop any tasks\nWith just a search and click!""")

        if App.is_auth:
            self.frame_right = taskmanagement_frame.TaskManager(master=self, corner_radius=5)
            self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        else:
            self.frame_right = ctk.CTkFrame(master=self, corner_radius=5)
            self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
            self._info = ctk.CTkLabel(master=self.frame_right,
                                    text="Manage almost all tasks on your computer\nWith just a click!", 
                                    justify='center', font=("Roboto Medium", 24))
            self._info.grid(row=0, column=0, columnspan=2, pady=200, padx=150, sticky="nsew")
            
            self.Frame1 = ctk.CTkFrame(self.frame_right)
            self.Frame1.place(relx=0.133, rely=0.62, relheight=0.235, relwidth=0.75)

            self.Button4 = ctk.CTkButton(self.Frame1)
            self.Button4.place(relx=0.15, rely=0.60, relheight=0.25, relwidth=0.70)
            self.Button4.configure(text='''Login''', command=self.home_)

            self.Label4 = ctk.CTkLabel(self.Frame1)
            self.Label4.place(relx=0.01, rely=0.20, relheight=0.15, relwidth=0.98)
            self.Label4.configure(text='''Login to manage and/or run tasks on your computer''')


    def change_appearance_mode(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


    def on_closing(self, event=0):
        self.destroy()


    def home_(self):
        if App.is_auth:
            self.home(True)
        self.home(False)


if __name__ == "__main__":
    app = App()
    vars_.APP = app
    app.mainloop()