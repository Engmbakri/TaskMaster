import mysql.connector
from config import DB_CONFIG
import hashlib

def get_database_connection():
    return mysql.connector.connect(**DB_CONFIG)

def create_task(title, description, due_date, username):
    conn = get_database_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO tasks (title, description, due_date, username) VALUES (%s, %s, %s, %s)"
    task_data = (title, description, due_date, username)
    cursor.execute(sql, task_data)
    conn.commit()
    cursor.close()
    conn.close()

def get_task(task_id):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM tasks WHERE id = %s"
    cursor.execute(sql, (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    return task

def update_task(task_id, title=None, description=None, due_date=None, status=None):
    conn = get_database_connection()
    cursor = conn.cursor()
    updates = []
    update_data = []

    if title:
        updates.append("title = %s")
        update_data.append(title)
    if description:
        updates.append("description = %s")
        update_data.append(description)
    if due_date:
        updates.append("due_date = %s")
        update_data.append(due_date)
    if status:
        updates.append("status = %s")
        update_data.append(status)

    if updates:
        sql = "UPDATE tasks SET " + ", ".join(updates) + " WHERE id = %s"
        update_data.append(task_id)
        cursor.execute(sql, tuple(update_data))
        conn.commit()

    cursor.close()
    conn.close()

def delete_task_from_db(task_id):
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Delete the task with the given ID from the 'tasks' table
        sql = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(sql, (task_id,))
        conn.commit()
    except mysql.connector.Error as err:
        print("Error:", err)
    finally:
        cursor.close()
        conn.close()


def signup(username, email, password):
    conn = get_database_connection()
    cursor = conn.cursor()
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, email, hashed_password))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        cursor.close()
        conn.close()

def login(username, password):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        sql = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(sql, (username, hashed_password))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_tasks_for_user(username):
    conn = get_database_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        sql = "SELECT * FROM tasks WHERE username = %s"
        cursor.execute(sql, (username,))
        tasks = cursor.fetchall()
        return tasks
    except mysql.connector.Error as err:
        print("Error:", err)
        return []
    finally:
        cursor.close()
        conn.close()
