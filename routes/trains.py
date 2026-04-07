from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app import mysql

trains = Blueprint('trains', __name__)

@trains.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    results = []
    if request.method == 'POST':
        source = request.form['source']
        destination = request.form['destination']
        date = request.form['date']
        cur = mysql.connection.cursor()
        cur.execute("""SELECT * FROM trains WHERE source=%s AND destination=%s
                       AND available_seats > 0 AND status='active'""", (source, destination))
        results = cur.fetchall()
        cur.close()
        return render_template('search.html', results=results, source=source,
                               destination=destination, date=date)
    return render_template('search.html', results=results)
