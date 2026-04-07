from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import mysql
from functools import wraps

admin = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated

@admin.route('/')
@admin_required
def dashboard():
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) as count FROM users WHERE role='user'")
    users = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM trains WHERE status='active'")
    active_trains = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM bookings WHERE status='confirmed'")
    confirmed = cur.fetchone()['count']
    cur.execute("SELECT COUNT(*) as count FROM bookings WHERE status='cancelled'")
    cancelled = cur.fetchone()['count']
    cur.close()
    return render_template('admin/dashboard.html', users=users,
                           active_trains=active_trains, confirmed=confirmed, cancelled=cancelled)

@admin.route('/trains')
@admin_required
def manage_trains():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM trains ORDER BY id DESC")
    all_trains = cur.fetchall()
    cur.close()
    return render_template('admin/trains.html', trains=all_trains)

@admin.route('/trains/add', methods=['GET', 'POST'])
@admin_required
def add_train():
    if request.method == 'POST':
        data = (request.form['train_number'], request.form['train_name'],
                request.form['source'], request.form['destination'],
                request.form['departure_time'], request.form['arrival_time'],
                request.form['total_seats'], request.form['total_seats'],
                request.form['fare'], request.form['run_days'])
        cur = mysql.connection.cursor()
        try:
            cur.execute("""INSERT INTO trains (train_number, train_name, source, destination,
                           departure_time, arrival_time, total_seats, available_seats, fare, run_days)
                           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
            mysql.connection.commit()
            flash('Train added successfully.', 'success')
            return redirect(url_for('admin.manage_trains'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
        finally:
            cur.close()
    return render_template('admin/add_train.html')

@admin.route('/trains/toggle/<int:train_id>')
@admin_required
def toggle_train(train_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT status FROM trains WHERE id=%s", (train_id,))
    train = cur.fetchone()
    new_status = 'inactive' if train['status'] == 'active' else 'active'
    cur.execute("UPDATE trains SET status=%s WHERE id=%s", (new_status, train_id))
    mysql.connection.commit()
    cur.close()
    flash(f'Train status updated to {new_status}.', 'success')
    return redirect(url_for('admin.manage_trains'))

@admin.route('/bookings')
@admin_required
def all_bookings():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT b.*, u.name as user_name, u.email, t.train_name, t.train_number,
                   t.source, t.destination FROM bookings b
                   JOIN users u ON b.user_id = u.id
                   JOIN trains t ON b.train_id = t.id
                   ORDER BY b.booked_at DESC""")
    all_b = cur.fetchall()
    cur.close()
    return render_template('admin/bookings.html', bookings=all_b)
