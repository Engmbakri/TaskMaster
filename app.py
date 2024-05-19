from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import create_task, get_task, update_task, delete_task_from_db, get_all_tasks_for_user, signup, login
import mysql.connector

app = Flask(__name__)
app.secret_key = '0123'

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        tasks = get_all_tasks_for_user(username)
        return render_template('index.html', tasks=tasks)
    else:
        return redirect(url_for('login_page'))

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            if signup(username, email, password):
                flash('Signup successful! Please log in.')
                return redirect(url_for('login_page'))
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Duplicate entry error
                flash('Username already exists. Please choose a different username.')
            else:
                flash('An error occurred. Please try again later.')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login(username, password):
            session['username'] = username
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
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
        username = session['username']  # Get the username from the session
        create_task(title, description, due_date, username)
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
        update_task(task_id, title=title, description=description, due_date=due_date, status=status)
        return redirect(url_for('view_task', task_id=task_id))
    return render_template('edit_task.html', task=task)

@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    # Call the delete_task function from db.py to delete the task
    delete_task_from_db(task_id)
    
    # Redirect to the homepage after deleting the task
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
