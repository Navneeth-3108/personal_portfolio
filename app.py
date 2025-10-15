import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from flask_mail import Mail, Message
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = bool(os.getenv('MAIL_USE_TLS'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)

db = client["Portfolio"]
collection = db["Contact_Form"]

@app.route('/')
def show_form():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def handle_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    collection.insert_one({
        'name': name,
        'email': email,
        'message': message
    })
    
    msg = Message(
        subject='New Contact Form Submission from Portfolio Site',
        sender=app.config['MAIL_USERNAME'],
        recipients=[app.config['MAIL_USERNAME']],
        body=f"Name: {name}\nEmail: {email}\nMessage: {message}"
    ) 
    mail.send(msg)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
