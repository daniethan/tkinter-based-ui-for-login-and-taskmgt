import smtplib, socket
from tkinter import messagebox
from email.message import EmailMessage
from random import randrange
from decouple import config

def generate_otp():
    otp = randrange(start=100001, stop=999999, step=1)
    return otp


def is_connected(host='smtp.gmail.com', port=587):
    try:
        #try to connect to the host to check if it's reachable
        sock = socket.create_connection(address=(host, port), timeout=2)
        if sock is not None:
            # close the socket
            sock.close
        return True
    except Exception as err:
        messagebox.showerror("Connection Failed", f"Something went wrong!\nPossibly no/unstable internet connection")
    return False


def send_otp_via_email(receipient: str):
    #check for internet connection and reachability of the host 
    #such that otp is only generated and sent when we are sure there is internet connection
    if is_connected():
        #generate the content (the OTP)
        otp = generate_otp()

        #prepare your message to be sent
        msg = EmailMessage()
        msg['to'] = receipient
        msg['subject'] = 'Required OTP to complete Login'
        msg.set_content(
            f"Your OTP is: {otp}"
        )

        #prepare sender email credentials
        username = config('EMAIL_SENDER')
        password = config('APP_PASSWORD')

        #setup the server connection
        server = smtplib.SMTP(host='smtp.gmail.com', port=config('EMAIL_PORT', cast=int))
        server.starttls()

        #logging in sender
        server.login(user=username, password=password)

        #send the email
        server.send_message(msg=msg, from_addr=username)

        #close the server connection
        server.quit()
        
        return otp
    else:
        messagebox.showerror("No Internet Connection", "Make sure you have stable internet connection and try again!.")
        return None