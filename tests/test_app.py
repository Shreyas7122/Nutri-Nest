import unittest
from app import app, mysql

class FlaskAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup for all tests."""
        cls.app = app
        cls.client = cls.app.test_client()
        cls.app.config['TESTING'] = True
        cls.app.config['MYSQL_DB'] = 'home_kitchen_db'
        cls.app.config['MYSQL_HOST'] = 'knivespc'
        cls.app.config['MYSQL_USER'] = 'root'
        cls.app.config['MYSQL_PASSWORD'] = 'sss27'
        
        # Initialize MySQL with test database
        cls.mysql = mysql
        cls.create_test_db()

    @classmethod
    def tearDownClass(cls):
        """Tear down after all tests."""
        cls.drop_test_db()

    @classmethod
    def create_test_db(cls):
        """Create a test database and populate it with initial data."""
        # Connect to MySQL and create a test database, tables, and sample data
        conn = mysql.connection.cursor()
        conn.execute('CREATE DATABASE IF NOT EXISTS test_home_kitchen_db')
        conn.execute('USE test_home_kitchen_db')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL
            )
        ''')
        conn.execute('INSERT INTO users (email, password) VALUES (%s, %s)', ('test@example.com', 'password123'))
        mysql.connection.commit()
        conn.close()

    @classmethod
    def drop_test_db(cls):
        """Drop the test database."""
        conn = mysql.connection.cursor()
        conn.execute('DROP DATABASE IF EXISTS test_home_kitchen_db')
        mysql.connection.commit()
        conn.close()

    def test_index(self):
        """Test the index route."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to NutriNest', response.data)  # Adjust based on your actual HTML content

    def test_contact(self):
        """Test the contact route."""
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Contact Us', response.data)  # Adjust based on your actual HTML content

    def test_login_page(self):
        """Test the login page route."""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Adjust based on your actual HTML content

    def test_login_valid(self):
        """Test login with valid credentials."""
        response = self.client.post('/login', data=dict(email='test@example.com', password='password123'))
        self.assertEqual(response.status_code, 302)  # Redirect status code
        self.assertEqual(response.location, url_for('menu', _external=True))

    def test_login_invalid(self):
        """Test login with invalid credentials."""
        response = self.client.post('/login', data=dict(email='wrong@example.com', password='wrongpassword'))
        self.assertEqual(response.status_code, 401)  # Unauthorized status code

    def test_about(self):
        """Test the about page route."""
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        
