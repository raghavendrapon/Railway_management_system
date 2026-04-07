from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import mysql
import random, string

bookings = Blueprint('bookings', __name__)

def generate_pnr():
    return 'PNR' + ''.join(random.choices(string.digits, k=8))

@bookings.route('/book/<int:train_id>', methods=['GET', 'POST'])
def book(train_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM trains WHERE id=%s", (train_id,))
    train = cur.fetchone()
    if request.method == 'POST':
        journey_date = request.form['journey_date']
        passenger_name = request.form['passenger_name']
        passenger_age = request.form['passenger_age']
        passenger_gender = request.form['passenger_gender']
        pnr = generate_pnr()
        seat = f"S{random.randint(1, train['total_seats'])}"
        cur.execute("""INSERT INTO bookings (pnr, user_id, train_id, journey_date,
                       passenger_name, passenger_age, passenger_gender, seat_number)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                    (pnr, session['user_id'], train_id, journey_date,
                     passenger_name, passenger_age, passenger_gender, seat))
        cur.execute("UPDATE trains SET available_seats = available_seats - 1 WHERE id=%s", (train_id,))
        mysql.connection.commit()
        cur.close()
        flash(f'Booking confirmed! Your PNR is {pnr}', 'success')
        return redirect(url_for('bookings.history'))
    cur.close()
    return render_template('book.html', train=train)

@bookings.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    cur = mysql.connection.cursor()
    cur.execute("""SELECT b.*, t.train_name, t.train_number, t.source, t.destination,
                   t.departure_time, t.fare FROM bookings b
                   JOIN trains t ON b.train_id = t.id
                   WHERE b.user_id=%s ORDER BY b.booked_at DESC""", (session['user_id'],))
    my_bookings = cur.fetchall()
    cur.close()
    return render_template('history.html', bookings=my_bookings)

@bookings.route('/cancel/<int:booking_id>')
def cancel(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM bookings WHERE id=%s AND user_id=%s", (booking_id, session['user_id']))
    booking = cur.fetchone()
    if booking and booking['status'] == 'confirmed':
        cur.execute("UPDATE bookings SET status='cancelled' WHERE id=%s", (booking_id,))
        cur.execute("UPDATE trains SET available_seats = available_seats + 1 WHERE id=%s", (booking['train_id'],))
        mysql.connection.commit()
        flash('Booking cancelled successfully.', 'success')
    else:
        flash('Cannot cancel this booking.', 'danger')
    cur.close()
    return redirect(url_for('bookings.history'))

@bookings.route('/pnr', methods=['GET', 'POST'])
def pnr_status():
    booking = None
    if request.method == 'POST':
        pnr = request.form['pnr']
        cur = mysql.connection.cursor()
        cur.execute("""SELECT b.*, t.train_name, t.train_number, t.source, t.destination,
                       t.departure_time, t.arrival_time, t.fare FROM bookings b
                       JOIN trains t ON b.train_id = t.id WHERE b.pnr=%s""", (pnr,))
        booking = cur.fetchone()
        cur.close()
        if not booking:
            flash('PNR not found.', 'danger')
    return render_template('pnr.html', booking=booking)
