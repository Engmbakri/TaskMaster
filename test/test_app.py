import unittest
from flask import url_for
from app import app, db
from app.models import Task  # Ensure you import the Task model if it's defined in app.models

class TaskMasterTestCase(unittest.TestCase):
    def setUp(self):
        # Set up test client and other test configuration
        app.config['TESTING'] = True
        app.config['MAIL_SUPPRESS_SEND'] = True  # suppress sending emails during tests
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # Clean up after each test
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_index_page(self):
        response = self.client.get(url_for('index'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_signup(self):
        response = self.client.post(url_for('signup_route'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Signup successful!', response.data)

    def test_login(self):
        self.client.post(url_for('signup_route'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        response = self.client.post(url_for('login_page'), data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_password_reset_request(self):
        response = self.client.post(url_for('password_reset_request'), data={
            'email': 'test@example.com'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'A password reset link has been sent to your email.', response.data)

    def test_create_task(self):
        self.client.post(url_for('signup_route'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.client.post(url_for('login_page'), data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        response = self.client.post(url_for('create_new_task'), data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2024-12-31',
            'priority': 'High'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Task', response.data)

    def test_edit_task(self):
        # First, create a task
        self.client.post(url_for('signup_route'), data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.client.post(url_for('login_page'), data={
            'username': 'testuser',
            'password': 'testpassword'
        }, follow_redirects=True)
        self.client.post(url_for('create_new_task'), data={
            'title': 'Test Task',
            'description': 'This is a test task',
            'due_date': '2024-12-31',
            'priority': 'High'
        }, follow_redirects=True)

        # Fetch the task ID
        task = db.session.query(Task).filter_by(title='Test Task').first()
        task_id = task.id

        # Now, edit the task
        response = self.client.post(url_for('edit_task', task_id=task_id), data={
            'title': 'Updated Test Task',
            'description': 'This is an updated test task',
            'due_date': '2025-01-01',
            'status': 'In Progress',
            'priority': 'Low'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Updated Test Task', response.data)

    def test_delete_task(self):
    # First, create and login the user
    self.client.post(url_for('signup.html'), data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'testpassword'
    })
    self.client.post(url_for('login_page'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)

    # Create a task
    self.client.post(url_for('create_new_task'), data={
        'title': 'Test Task',
        'description': 'This is a test task',
        'due_date': '2024-12-31',
        'priority': 'High'
    }, follow_redirects=True)

    # Fetch the task ID
    task = db.session.query(Task).filter_by(title='Test Task').first()
    task_id = task.id

    # Now, delete the task
    response = self.client.post(url_for('delete_task', task_id=task_id), follow_redirects=True)
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Task has been deleted', response.data)

    # Verify the task is deleted
    deleted_task = db.session.query(Task).filter_by(id=task_id).first()
    self.assertIsNone(deleted_task)
