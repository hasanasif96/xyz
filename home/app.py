from flask import Flask, request, render_template
from pymongo import MongoClient
import requests
import os

app = Flask(__name__)
#password="xlO7WEk33f65Dsdr"
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

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form['email']
        collection.insert_one({'email': email})
        send_email_service_url = 'http://send-mail-service:5001/'
        response = requests.get(send_email_service_url)

        if response.status_code == 200:
            return "Email saved and sent successfully!"
        else:
            return "Failed to send email."
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
