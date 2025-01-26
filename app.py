from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
import MySQLdb.cursors
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            account = cursor.fetchone()
            cursor.close()
            if account and check_password_hash(account['password'], password):
                role = account['role']
                if role == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('menu'))
            else:
                flash('Invalid credentials', 'error')
        except MySQLdb.Error as e:
            flash(f"Database error: {e}", 'error')
        return redirect(url_for('login_page'))
    return render_template('login.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/admin')
def admin_dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM checkouts')
    checkout_details = cursor.fetchall()
    cursor.close()
    return render_template('admin_dashboard.html', checkout_details=checkout_details)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        city = request.form.get('city')
        zip_code = request.form.get('zip')
        delivery_preference = request.form.get('delivery_preference')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'INSERT INTO checkouts (name, email, address, city, zip_code, delivery_preference) VALUES (%s, %s, %s, %s, %s, %s)',
            (name, email, address, city, zip_code, delivery_preference)
        )
        mysql.connection.commit()
        cursor.close()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('checkout'))

    # Retrieve all checkout data to display
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM checkouts')
    checkout_details = cursor.fetchall()
    cursor.close()
    return render_template('checkout.html', checkout_details=checkout_details)



@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    role = request.form['role']
    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('login_page'))
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    if account:
        flash('Account already exists', 'error')
    else:
        cursor.execute('INSERT INTO users (email, password, role) VALUES (%s, %s, %s)', (email, hashed_password, role))
        mysql.connection.commit()
        flash('Account created successfully', 'success')
    cursor.close()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
