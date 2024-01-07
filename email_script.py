import pyrebase
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google_auth_oauthlib.flow import *
from google.oauth2 import id_token
import pathlib
import requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

config = {
    "apiKey": "AIzaSyD5RIIvVplUAgs-j6aKswDGduO7hu60yPk",
    "authDomain": "stocknews-4fdd8.firebaseapp.com",
    "databaseURL": "https://stocknews-4fdd8-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "stocknews-4fdd8",
    "storageBucket": "stocknews-4fdd8.appspot.com",
    "messagingSenderId": "341949545648",
    "appId": "1:341949545648:web:de050fe16458479451cf75",
    "measurementId": "G-NYD8790VVL"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

def send_email(symbol_df):
    col_list = symbol_df.columns
    comp_symbol = list(symbol_df[col_list[0]])
    comp_name = list(symbol_df[col_list[1]])
    announcement_subject = list(symbol_df[col_list[2]])
    details = list(symbol_df[col_list[3]])
    attachement_link = list(symbol_df[col_list[8]])
    broadcast_datetime = list(symbol_df[col_list[4]])
    for i in range(len(comp_symbol)):
        sym = comp_symbol[i]
        print(sym)
        subs = db.child("stock_subscribers").child(sym).child("subscribers").get()
        try:
            subs_val = subs.val().values()
            subs_keys = subs.val().keys()
            print(subs_keys)
            print(subs_val)
            receiver_email = []

            for sub in subs_val:
                # Make an API call to get the user's email address
                # print(sub)
                sub_info = db.child("user_information").child(sub).get()
                print(list(sub_info.val().values())[0]['email'])
                curr_email = list(sub_info.val().values())[0]['email']
                receiver_email.append(curr_email)

            print(receiver_email)
            # Email configuration
            sender_email = 'lokeshbamb@gmail.com'
            #receiver_email = ['bamb.1@iitj.ac.in','lokeshbamb@gmail.com', 'kapoor.3@iitj.ac.in']
            subject = 'Corporate Announcement for ' + comp_name[i]
            message = str(comp_name[i]) + '\n\n' + 'Brief: ' + str(announcement_subject[i]) + '\n\nDescription:\n' + str(details[i]) + '\n\nAnnouncement made on ' + str(broadcast_datetime[i]) + '\n\nAnnouncement Link: ' + str(attachement_link[i]) + '\n\nThanks,\nStockNews.'

            # Create a MIMEText object
            msg = MIMEMultipart()
            msg['From'] = sender_email
            # msg['Bcc'] = ', '.join(receiver_email)
            msg['Subject'] = subject

            # Attach the message to the MIMEText object
            msg.attach(MIMEText(message, 'plain'))

            # SMTP server configuration (for Gmail)
            smtp_server = 'smtp.gmail.com'
            smtp_port = 587
            smtp_username = 'lokeshbamb@gmail.com'
            smtp_password = 'fpgi jmzz yjdo xcmr'  # Use an 'App Password' if you have 2-factor authentication enabled

            # Establish a secure connection with the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                
                # Send the email
                server.sendmail(sender_email, receiver_email, msg.as_string())

            print('Email sent successfully for', sym)
        except:
            print("Stock Not added on firebase", sym)