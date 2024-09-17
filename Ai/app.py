from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",       # Replace with your MySQL host
    user="root",            # Replace with your MySQL username
    password="root",        # Replace with your MySQL password
    database="event_registration_db"  # Replace with your database name
)

# Route to load the registration form
@app.route('/')
def registration_form():
    return render_template('reg.html')  # Renders the reg.html page

# Route to handle form submission
@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    # Get form data
    full_name = request.form['full_name']
    phone = request.form['phone']
    email = request.form['email']
    branch = request.form['branch']
    year = request.form['year']
    event_name = request.form['event_name']
    team_size = request.form['team_size']
    transaction_id = request.form['transaction_id']

    # Insert form data into the MySQL database
    cursor = db.cursor()
    sql = "INSERT INTO participants (full_name, phone, email, branch, year, event_name, team_size, transaction_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val = (full_name, phone, email, branch, year, event_name, team_size, transaction_id)
    cursor.execute(sql, val)
    db.commit()
    cursor.close()

    # Show success message
    success_message = "Registration successful! Data saved to the database."
    
    return render_template('reg.html', success_message=success_message)  # Display success message

# Route to display the dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Renders the dashboard.html page

# Route to load data from the MySQL database to display on the dashboard
@app.route('/load_csv', methods=['GET'])
def load_csv():
    # Query the data from the MySQL database
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM participants")
    rows = cursor.fetchall()  # Fetch all rows from the query result
    cursor.close()

    # Send the data as JSON response
    return jsonify(rows)

if __name__ == '__main__':
    app.run(debug=True)
