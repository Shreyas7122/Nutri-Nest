from flask import Flask, request, redirect, url_for, render_template, flash
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

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
    account = cursor.fetchone()
    cursor.close()
    if account and check_password_hash(account['password'], password):
        return redirect(url_for('menu'))
    else:
        flash('Invalid credentials', 'error')
        return redirect(url_for('login_page'))

@app.route('/menu')
def menu():
    return render_template('menu.html')

# Route to display the checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # Retrieve cart data from the POST request
        cart_data = request.get_json()
        # Store cart data in session (or pass directly)
        if cart_data:
            # Redirect to the checkout page
            return jsonify({"redirect": url_for('checkout')})
        else:
            return jsonify({"error": "No cart data received"}), 400
    else:
        # For GET requests, render the checkout page
        return render_template('checkout.html')

def process_checkout():
    # Retrieve form data
    name = request.form.get('name')
    email = request.form.get('email')
    address = request.form.get('address')
    city = request.form.get('city')
    zip_code = request.form.get('zip')
    card_number = request.form.get('cardNumber')
    expiry_date = request.form.get('expiryDate')
    cvv = request.form.get('cvv')

    # Process the order
    # Example: Save to database, send an email, etc.

    return redirect(url_for('menu'))  # Redirect to a success page or menu

@app.route('/redirect_to_checkout') 
def redirect_to_checkout(): return redirect(url_for('checkout'))

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
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
        cursor.execute('INSERT INTO users (email, password) VALUES (%s, %s)', (email, hashed_password))
        mysql.connection.commit()
        flash('Account created successfully', 'success')
    cursor.close()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)
