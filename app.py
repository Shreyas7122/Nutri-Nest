# app.py
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'knivespc'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'sss27'
app.config['MYSQL_DB'] = 'home_kitchen_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
def lgoinh():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
    account = cursor.fetchone()
    if account:
        return redirect(url_for('menu'))
    else:
        return 'Invalid credentials', 401

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        return 'Passwords do not match', 400
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account:
        return 'Account already exists', 400

    cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
    mysql.connection.commit()
    cursor.close()
    return render_template('menu.html')

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        return 'Passwords do not match', 400
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account:
        return 'Account already exists', 400

    cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, password))
    mysql.connection.commit()
    cursor.close()
    
    # Return a small HTML page with JavaScript to redirect and check the checkbox
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)
  