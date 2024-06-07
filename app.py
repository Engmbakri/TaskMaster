from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mail import Mail, Message
from db import create_task, get_task, update_task, delete_task_from_db, get_all_tasks_for_user, signup, login, get_user_by_email, update_password
from itsdangerous import URLSafeTimedSerializer
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Email configurations
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_reset_token(user_id):
    return s.dumps(user_id, salt='password-reset-salt')

def send_reset_email(email, token):
    msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[email])
    link = url_for('reset_password', token=token, _external=True)
    msg.body = f'''To reset your password, visit the following link:
{link}

If you did not make this request, please ignore this email.
'''
    mail.send(msg)

def verify_reset_token(token, expiration=3600):
    try:
        user_id = s.loads(token, salt='password-reset-salt', max_age=expiration)
        return user_id
    except:
        return None

@app.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    if request.method == 'POST':
        email = request.form['email']
        user = get_user_by_email(email)
        if user:
            token = generate_reset_token(user['id'])
            send_reset_email(user['email'], token)
            flash('A password reset link has been sent to your email.', 'success')
        else:
            flash('No account found with that email address.', 'error')
    return render_template('password_reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = verify_reset_token(token)
    if not user_id:
        flash('The password reset link is invalid or has expired.', 'error')
        return redirect(url_for('password_reset_request'))

    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('reset_password', token=token))

        update_password(user_id, password)
        flash('Your password has been reset successfully!', 'success')
        return redirect(url_for('login_page'))

    return render_template('reset_password.html', token=token)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        tasks = get_all_tasks_for_user(username)
        return render_template('index.html', tasks=tasks)
    else:
        return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET', 'POST'])
def signup_route():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            if signup(username, email, password):
                session['username'] = username
                flash('Signup successful! Please log in.', 'success')
                return redirect(url_for('login_page'))
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error
                if 'username' in str(err):
                    flash('Username already exists. Please choose a different username.', 'error')
                elif 'email' in str(err):
                    flash('Email already exists. Please use a different email address.', 'error')
            else:
                flash('An error occurred. Please try again later.', 'error')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            session['username'] = username
            flash('Login Successfull!', 'Success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login_page'))

@app.route('/task/<int:task_id>')
def view_task(task_id):
    task = get_task(task_id)
    return render_template('task.html', task=task)

@app.route('/task/new', methods=['GET', 'POST'])
def create_new_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        priority = request.form['priority']
        username = session['username']
        create_task(title, description, due_date, username, priority)
        return redirect(url_for('index'))
    return render_template('new_task.html')

@app.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    task = get_task(task_id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        status = request.form['status']
        priority = request.form['priority']
        update_task(task_id, title=title, description=description, due_date=due_date, status=status, priority=priority)
        return redirect(url_for('view_task', task_id=task_id))
    return render_template('edit_task.html', task=task)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    delete_task_from_db(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 1000))  # Use PORT from environment or default to 5000
    app.run(host='0.0.0.0', port=port)
