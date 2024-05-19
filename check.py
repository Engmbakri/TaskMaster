from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mohammed'
app.config['MYSQL_PASSWORD'] = 'hmoodecr1o'
app.config['MYSQL_DB'] = 'task_management_db'

mysql = MySQL(app)

# Route to add information to the user table
@app.route('/add_user')
def add_user():
    try:
        # Establish a connection to MySQL
        cur = mysql.connection.cursor()

        # Insert data into the Users table
        cur.execute("INSERT INTO Users (username , email, password_hash) VALUES (engmohammed, 123456, 12lljjjj)", (value1, value2, value3))

        # Commit changes to the database
        mysql.connection.commit()

        # Close the cursor
        cur.close()

        return "User information added successfully!"
    except Exception as e:
        return "An error occurred: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)
