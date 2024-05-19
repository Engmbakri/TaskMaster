from flask_mysqldb import MySQL
import mysql.connector
import MySQLdb.cursors

# MySQL Connection Configuration
config = {
    'host': 'localhost',
    'user': 'mohammed',
    'password': 'hmoodecr1o',
    'database': 'task_management_db'
}

try:
    conn = mysql.connector.connect(**config)
    if conn.is_connected():
        print("MySQL connection established successfully!")
        conn.close()
    else:
        print("MySQL connection failed.")
except Exception as e:
    print("An error occurred:", e)
