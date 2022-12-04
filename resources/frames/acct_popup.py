import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk

from config import dbconfig, models
from resources.services.auth import validate_password
from resources.services import ext, otp_handler

class AccountCreator(ctk.CTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        '''This class configures and populates the toplevel window.
            top is the toplevel containing window.'''

        self.geometry("500x350+500+150")
        self.minsize(120, 1)
        self.resizable(0,  0)
        self.attributes('-alpha',0.97)
        self.title("Create Account and Auth PIN")

        self.pin1 = tk.IntVar()
        self.pin2 = tk.IntVar()

        self.Label1 = ctk.CTkLabel(self, font=("Roboto Medium", 20))
        self.Label1.place(relx=0.283, rely=0.065, height=30, width=254)
        self.Label1.configure(text='''Create Account''')

        self.Label2 = ctk.CTkLabel(self)
        self.Label2.place(relx=0.15, rely=0.26, height=22, width=114)
        self.Label2.configure(anchor='w')
        self.Label2.configure(text='''Name:''')

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.place(relx=0.378, rely=0.26, height=22, relwidth=0.457)

        self.Label3 = ctk.CTkLabel(self)
        self.Label3.place(relx=0.15, rely=0.34, height=22, width=114)
        self.Label3.configure(anchor='w')
        self.Label3.configure(text='''Email:''')

        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.place(relx=0.378, rely=0.34, height=22, relwidth=0.457)

        self.Label4 = ctk.CTkLabel(self)
        self.Label4.place(relx=0.15, rely=0.42, height=22, width=114)
        self.Label4.configure(anchor='w')
        self.Label4.configure(text='''Password:''')

        self.pass1_entry = ctk.CTkEntry(self, show='*')
        self.pass1_entry.place(relx=0.378, rely=0.42, height=22, relwidth=0.457)

        self.Label5 = ctk.CTkLabel(self)
        self.Label5.place(relx=0.15, rely=0.5, height=22, width=114)
        self.Label5.configure(anchor='w')
        self.Label5.configure(text='''Confirm Password:''')

        self.pass2_entry = ctk.CTkEntry(self, show='*')
        self.pass2_entry.place(relx=0.378, rely=0.5, height=22, relwidth=0.457)

        self.Label6 = ctk.CTkLabel(self)
        self.Label6.place(relx=0.15, rely=0.58, height=22, width=114)
        self.Label6.configure(anchor='w')
        self.Label6.configure(text='''Secret PIN (5-digit):''')

        self.pin1_entry = ctk.CTkEntry(self, textvariable=self.pin1, show='*')
        self.pin1_entry.place(relx=0.378, rely=0.58, height=22, relwidth=0.457)

        self.Label7 = ctk.CTkLabel(self)
        self.Label7.place(relx=0.15, rely=0.66, height=22, width=114)
        self.Label7.configure(anchor='w')
        self.Label7.configure(text='''Confirm secret PIN:''')

        self.pin2_entry = ctk.CTkEntry(self, textvariable=self.pin2, show='*')
        self.pin2_entry.place(relx=0.378, rely=0.66, height=22, relwidth=0.457)

        self.Button1 = ctk.CTkButton(self, font=("Roboto Medium", 12))
        self.Button1.place(relx=0.2, rely=0.83, relheight=0.1, relwidth=0.60)
        self.Button1.configure(text='''Validate''', command=self.on_submit)

    def on_submit(self):
        self.attributes('-topmost',0)
        #check the input data to ensure it's valid!
        user_input = {
                        'name': self.name_entry.get(),
                        'email': self.email_entry.get(),
                        'password': ext.Hash.encrypt(self.pass1_entry.get()),
                        'pin': ext.Hash.encrypt(self.pin1_entry.get())       
                        }
        #check for unfilled entries and mismatched pin and passwords
        for key in user_input.keys():
            if user_input.get(key)=='':
                messagebox.showerror(
                    'Required Fields Unfilled', 
                    'All fields are required\nPlease provide all the missing values.')
                self.attributes('-topmost',2)
                return
            #validate the email
            if key == 'email' and '@gmail.com' not in user_input.get(key):
                messagebox.showerror(
                'Unsupported Email Type', 
                "Sorry! This app only supports gmail email address!")
                self.attributes('-topmost',2)
                return
            #check for unmatched and invalid pins
            if key == 'pin':
                if type(self.pin1.get()) != int or type(self.pin2.get()) != int:
                    messagebox.showerror(
                        'Invalid PIN Type', 
                        "The PIN must be a 5-digit number not string")
                    self.attributes('-topmost',2)
                    return                   
                if len(self.pin1_entry.get()) != 5:  
                    messagebox.showerror(
                        'Invalid PIN Length', 
                        "The PIN must be a 5-digit number")
                    self.attributes('-topmost',2)
                    return
                elif not ext.Hash.verify_password(self.pin2_entry.get(), user_input.get(key)):
                    messagebox.showerror(
                        'Unmatched PINs', 
                        "The PINs provided don't much!")
                    self.attributes('-topmost',2)
                    return
            #check for unmatched and invalid passwords
            if key == 'password':
                if not ext.Hash.verify_password(self.pass2_entry.get(), user_input.get(key)):
                    messagebox.showerror(
                        'Unmatched Passwords', 
                        "The Passwords provided don't much!")
                    self.attributes('-topmost',2)
                    return
                if not validate_password(self.pass1_entry.get()):
                    messagebox.showerror(
                        'Invalid Password', 
                        "The Password must be at least 8 characters\ncontaining digits, uppercase and lowercase letters\nand at least one special character.")                    
                    self.attributes('-topmost',2)
                    return  

        db = dbconfig.session
        user_in_db = db.query(models.User).filter(models.User.email==user_input['email']).first()
        if user_in_db is not None:
            messagebox.showerror(
                'Email Already Taken', 
                f":> {user_input['email']}\nThe email provided above already belongs to another user")
            self.attributes('-topmost',2)
            return
        else:
            otp_sent = otp_handler.send_otp_via_email(receipient=user_input['email'])
            if otp_sent is not None:
                trials = 3
                while trials > 0:
                    otp_in = simpledialog.askinteger(
                                                    'Confirm Your Email', 
                                                    "Please enter the OTP just sent to your email\nto confirm your email.", 
                                                    minvalue=100001, 
                                                    maxvalue=999999
                                                    )
                    if otp_in != otp_sent:
                        #if the user just cancels entry of the OTP
                        if otp_in == '':
                            is_valid = False
                            break
                        trials -= 1
                        messagebox.showerror('Wrong OTP', f"Wrong OTP was entered!\nTry Again...({trials} left)")
                    
                    else:
                        is_valid = True
                        messagebox.showinfo('Success', "Account Created Successfully!")
                        break
                else:
                    is_valid = False
                    messagebox.showerror('Trials Depleted', f"Wrong OTP was entered 3 times!\nTry again later...")
            else:
                is_valid = False            
        
        if is_valid:
            user = models.User(
                name=self.name_entry.get(),
                email=self.email_entry.get(),
                password=ext.Hash.encrypt(self.pass1_entry.get()),
                pin=ext.Hash.encrypt(self.pin1_entry.get())
            )

            db.add(user)
            db.commit()
            db.refresh(user)

            self.close_app()
    
    def close_app(self):
        self.destroy()