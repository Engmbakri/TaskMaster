TaskMaster

TaskMaster is a task management web application built with Flask. It allows users to sign up, log in, create, edit, and delete tasks. Each task can have a title, description, due date, status, and priority.

Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Project Structure](#project-structure)

Introduction

TaskMaster was inspired by the need for a straightforward and efficient tool to manage tasks. This project demonstrates the use of Flask for building a web application, MySQL for database management, and includes user authentication and task CRUD operations.

Features

- User Authentication (Sign Up, Log In, Log Out)
- Create, Read, Update, and Delete Tasks
- Assign Priorities and Due Dates to Tasks
- Password Reset Functionality

Installation

Prerequisites

- Python 3.8+
- MySQL
- pip (Python package installer)

Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/Engmbakri/taskmaster.git
    cd taskmaster
    ```

2. Create a virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    Create a MySQL database and a user with access to this database. Update your `.env` file with the appropriate database configuration:

    ```
    MAIL_USERNAME=your-email@gmail.com
    MAIL_PASSWORD=your-email-password
    SECRET_KEY=your-secret-key
    DB_HOST=localhost
    DB_PORT=3306
    DB_USER=your-db-user
    DB_PASSWORD=your-db-password
    DB_NAME=task_manager
    ```

5. **Initialize the database:**

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

6. Run the application:


## Usage

1. Sign Up:

    Go to the sign-up page and create a new account.

2. Log In:

    Log in with your credentials.

3. Create Task:

    Create new tasks by providing the title, description, due date, and priority.

4. Edit Task:

    Edit existing tasks to update their details.

5. Delete Task:

    Delete tasks that are no longer needed.

6. Password Reset:

    Request a password reset link if you forget your password.

## Running Tests

To run the tests, use the following command:

```bash
python3 -m unittest discover -s tests
Deployment
Deploying on Render.com
Create a new Web Service:

Go to Render.com and sign up or log in.
Click on "New" and select "Web Service".
Connect your GitHub repository containing the TaskMaster project.
Configure the service:

Set the build command to pip install -r requirements.txt.
Set the start command to flask run --host=0.0.0.0 --port=$PORT.
Add environment variables as defined in your .env file.

taskmaster/
│
├── app.py              # Main application file
├── db.py               # Database interaction logic
├── config.py           # Configuration file
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
└── tests/              # Unit tests

This project is licensed under the MIT License. See the LICENSE file for details.
