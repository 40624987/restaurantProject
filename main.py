
# main.py
import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import func

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session-based flash messages

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservations.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Reservation Model
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    guests = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Reservation {self.name} on {self.date}>"

# Create tables in the database
with app.app_context():
    db.create_all()

@app.route('/view_reservations')
def view_all_reservations():
    # Fetch all reservations from the database using SQLAlchemy
    reservations = Reservation.query.all()
    return render_template('admin.html', reservations=reservations)

# Route for home page
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

# Route for about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for admin page
@app.route('/admin', defaults={'page': 1})
@app.route('/admin/page/<int:page>', methods=['GET'])
def admin(page):
    per_page = 10
    filter_type = request.args.get('filter_type')
    filter_value = request.args.get('filter_value')

    query = Reservation.query

    # Apply filters based on filter_type
    if filter_type and filter_value:
        if filter_type == 'day':
            # Filter by exact date (e.g., "2024-12-09")
            try:
                filter_value = datetime.strptime(filter_value, '%Y-%m-%d').date()
                query = query.filter(Reservation.date == filter_value)
            except ValueError:
                return "Invalid date format. Please use YYYY-MM-DD.", 400
        elif filter_type == 'month':
            # Filter by month (e.g., "2024-12" for December 2024)
            try:
                filter_value = datetime.strptime(filter_value, '%Y-%m').strftime('%Y-%m')
                query = query.filter(func.strftime('%Y-%m', Reservation.date) == filter_value)
            except ValueError:
                return "Invalid month format. Please use YYYY-MM.", 400
        elif filter_type == 'hour':
            # Filter by hour (e.g., "14:00" for 2:00 PM)
            query = query.filter(Reservation.time == filter_value)

    reservations = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin.html', reservations=reservations)


@app.route('/admin/view_reservations')
def view_reservations():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM reservations")
    reservations = c.fetchall()  # Get all reservations
    conn.close()

    return render_template('admin.html', reservations=reservations)


# Route for reservation page
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        time = request.form['time']
        guests = request.form['guests']

        # Create a new reservation object
        new_reservation = Reservation(name=name, email=email, date=date, time=time, guests=guests)

        # Add the reservation to the database
        db.session.add(new_reservation)
        db.session.commit()




        return redirect(url_for('home'))  # Redirect to home after submission

    return render_template('reservation.html')

# Route for editing a reservation
@app.route('/admin/edit_reservation/<int:id>', methods=['GET', 'POST'])
def edit_reservation(id):
    reservation = Reservation.query.get(id)
    if request.method == 'POST':
        # Update the reservation details
        reservation.name = request.form['name']
        reservation.email = request.form['email']
        reservation.date = request.form['date']
        reservation.time = request.form['time']
        reservation.guests = request.form['guests']

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('edit_reservation.html', reservation=reservation)

# Route for deleting a reservation
@app.route('/admin/delete_reservation/<int:id>', methods=['GET'])
def delete_reservation(id):
    reservation = Reservation.query.get(id)
    if reservation:
        db.session.delete(reservation)
        db.session.commit()
    return redirect(url_for('admin'))

# Route for login page
@app.route('/login')
def login():
    return render_template('login.html')

# Route for menu page
@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
