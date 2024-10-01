from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'wixx.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'wixx'
app.config['MYSQL_PASSWORD'] = 'system'
app.config['MYSQL_DB'] = 'wixx$db_1'

mysql = MySQL(app)
app.secret_key = 'your_secret_key'  # Used to encrypt session data

@app.route('/')
def home():
    return redirect(url_for('signup_email'))

# Step 1: Email input page
@app.route('/signup_email', methods=['GET', 'POST'])
def signup_email():
    if request.method == 'POST':
        session['email'] = request.form['email']  # Save email in session
        return redirect(url_for('signup_password'))  # Redirect to the password page
    return render_template('index.html')

# Step 2: Password input page
@app.route('/signup_password', methods=['GET', 'POST'])
def signup_password():
    if request.method == 'POST':
        password = request.form['password']
        email = session.get('email')  # Retrieve the email from session

        # Insert email and password into the MySQL database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO signup (email, password) VALUES (%s, %s)', (email, password))
        mysql.connection.commit()
        cursor.close()

        # Clear session after signup
        session.pop('email', None)

        flash('Sign-up successful!', 'success')
        return render_template('success.html')

    return render_template('index2.html')

if __name__ == '__main__':
    app.run(debug=True)
