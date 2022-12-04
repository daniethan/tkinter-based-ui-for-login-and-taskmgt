import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk
from . import acct_popup
from resources.services import auth, otp_handler

class LoginFrame(ctk.CTkFrame): 
    def __init__(self, home, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.home = home

        self.frm_login = ctk.CTkFrame(self)
        self.frm_login.place(relx=0.10, rely=0.125, relheight=0.75, relwidth=0.80)

        self.Label1 = ctk.CTkLabel(self.frm_login, font=("Roboto Medium", 24))
        self.Label1.place(relx=0.15, rely=0.1, relheight=0.15, relwidth=0.70)
        self.Label1.configure(text='''SIGN IN''')

        self.Label2 = ctk.CTkLabel(self.frm_login, font=("Segoui UI", 12))
        self.Label2.place(relx=0.112, rely=0.34, height=25, width=74)
        self.Label2.configure(text='''Username:''')

        self.Label3 = ctk.CTkLabel(self.frm_login, font=("Segoui UI", 12))
        self.Label3.place(relx=0.112, rely=0.411, height=25, width=74)
        self.Label3.configure(text='''Password:''')

        self.Entry_name = ctk.CTkEntry(self.frm_login, textvariable=self.username)
        self.Entry_name.place(relx=0.292, rely=0.34, height=25, relwidth=0.593)

        self.Entry1_pass = ctk.CTkEntry(self.frm_login, textvariable=self.password, show='*')
        self.Entry1_pass.place(relx=0.292, rely=0.411, height=25, relwidth=0.593)

        self.Button1 = ctk.CTkButton(self.frm_login)
        self.Button1.place(relx=0.175, rely=0.575, relheight=0.1, relwidth=0.65)
        self.Button1.configure(text='''Login''', command=self.on_login)

        self.Button2 = ctk.CTkButton(self.frm_login, fg_color='green')
        self.Button2.place(relx=0.525, rely=0.8, relheight=0.098, relwidth=0.325)
        self.Button2.configure(command=self.on_btn_create_acct)
        self.Button2.configure(text='''Create Account''')

        self.Button3 = ctk.CTkButton(self.frm_login, fg_color='#0475f7')
        self.Button3.place(relx=0.135, rely=0.8, relheight=0.098, relwidth=0.325)
        self.Button3.configure(command=self.on_btn_forgot_password)
        self.Button3.configure(text='''Forgot Password''')

 
    def on_btn_forgot_password(self):
        send_feature_notice()
    
    def on_login(self):
        #check credentials
        is_auth = auth.check_credentials(username=self.username.get(), password = self.password.get())
        
        #invoke a messagebox to alert the user.
        if not is_auth:
            messagebox.showerror('Invalid Credentials', "Credentials provided not valid!")
        else:
            messagebox.showinfo('OTP On The Way', 'Valid Credentials.\nClose this box and wait for OTP via email.')
            otp_sent = otp_handler.send_otp_via_email(receipient=self.username.get())
            if otp_sent is not None:
                trials = 3
                while trials > 0:
                    otp_in = simpledialog.askinteger(
                                                    '2FA OTP', 
                                                    "Please enter the OTP just sent to your email", 
                                                    minvalue=100001, 
                                                    maxvalue=999999, 
                                                    )
                    if otp_in != otp_sent:
                        #is the user just cancels entry of the OTP
                        if otp_in is None:
                            # is_auth = False
                            break
                        else:
                            trials -= 1
                            messagebox.showerror('Wrong OTP', f"Wrong OTP was entered!\nTry Again...({trials} left)")
                    else:
                        is_auth = True
                        messagebox.showinfo('Success', "Login Successful!")
                        #load the home page
                        self.home(is_auth)
                        return
                else:
                    is_auth = False
                    messagebox.showerror('Trials Depleted', f"Wrong OTP was entered 3 times!\nTry again later...")
                    return
            else:
                return

    def on_btn_create_acct(self):
        popup = acct_popup.AccountCreator()
        popup.mainloop()
        

def send_feature_notice():
    messagebox.showwarning('Coming Soon!', "Sorry! Functionality to be added soon")
