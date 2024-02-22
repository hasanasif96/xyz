# service2.py
from flask import Flask
from pymongo import MongoClient
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

password = os.environ.get('MONGO_PASSWORD')
connection_str = "mongodb+srv://mailsforha:{password}@cluster1.osvjyqy.mongodb.net/"
#client = MongoClient(connection_str)
client = MongoClient(host=connection_str,
                         port=27017,
                         username='mailsforha',
                         password=password,
                        authSource="admin")
db = client['user_emails']
collection = db['emails']

def send_email(receiver_email):
    
    sender_email = os.environ.get('SMTP_USERNAME')  
    password = os.environ.get('SMTP_PASSWORD')

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, password)
    # message to be sent
    message = "Message_you_need_to_send"
    s.sendmail(sender_email, receiver_email, message)
    s.quit()



@app.route('/')
def send_emails():
    emails = collection.find()
    for email in emails:
        send_email(email['email'])
    return "Emails sent successfully!"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5001)
