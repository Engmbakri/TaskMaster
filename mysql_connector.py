import mysql.connector

# Establish a connection to the MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="mohammed",
    password="hmoodecr1o",
    database="task_management_db"
)

# Create a cursor
cursor = conn.cursor()

# Execute a query (non-parameterized)
cursor.execute("INSERT INTO Users (username, email, password_hash) VALUES ('done', 'done@example.com', 'ahbb15555488gg8')")
# ^ Notice the closing parenthesis after 'done@example.com'

# Commit the transaction
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()
