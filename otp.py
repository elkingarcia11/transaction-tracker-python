from flask import Flask
from flask_mail import Mail
from decouple import config

def main():
    port = 587
    smtp_server = 'smtp.gmail.com'
    sender_email = config('GMAIL_EMAIL')   
    receiver_email = config('RECEIVER_EMAIL')
    sender_password = config('GMAIL_PASSWORD')
    
    app = Flask(__name__)
    mail = Mail(app)
main()
