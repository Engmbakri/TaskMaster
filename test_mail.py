from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

# Email configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'altyebwebsite@gmail.com'
app.config['MAIL_PASSWORD'] = 'ufbu vbqk ykvl lpgn'

mail = Mail(app)

# Root route
@app.route('/')
def index():
    return 'Welcome to the Flask Email Sender! Go to /send-email to send an email.'

# Send email route
@app.route('/send-email')
def send_email():
    msg = Message('Hello from Flask',
                  sender='altyebwebsite@gmail.com',
                  recipients=['engbekoo10@gmail.com'])
    msg.body = 'This is a test email sent from a Flask web application!'
    mail.send(msg)
    return 'Email sent!'

if __name__ == '__main__':
    app.run(debug=True)
