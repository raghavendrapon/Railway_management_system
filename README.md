🚆 Railway Reservation Management System (Flask)

A complete Railway Reservation System built using Flask + MySQL with user booking, admin control, and PNR tracking.

📌 Features
🔐 User Registration & Login
🚆 Train Search & Availability
🎟️ Ticket Booking with PNR
❌ Cancel Booking
🔎 PNR Status Tracking
👨‍💼 Admin Dashboard
📊 Manage Trains & Bookings
🛠️ Tech Stack
Backend: Flask
Database: MySQL
Frontend: HTML + CSS
Libraries: Flask, Flask-MySQLdb, Werkzeug
📂 Project Structure
project/
│── app.py
│── config.py
│── requirements.txt
│── schema.sql
│
├── routes/
│   ├── auth.py
│   ├── trains.py
│   ├── bookings.py
│   └── admin.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── search.html
│   ├── book.html
│   ├── history.html
│   ├── pnr.html
│   └── admin/
│       ├── dashboard.html
│       ├── trains.html
│       ├── add_train.html
│       └── bookings.html
│
└── static/
    └── style.css
⚙️ Installation & Setup
git clone https://github.com/your-username/railway-management-system.git
cd railway-management-system

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
🗄️ Database Setup

Run the SQL file:
SOURCE schema.sql;
📌 Database contains:

users table → stores login & roles
trains table → train details
bookings table → ticket bookings

👉 Includes default admin:

Email: admin@rms.com
Password: admin123
▶️ Run the App
python app.py

Open:

http://127.0.0.1:5000/
🔍 File Explanation
🔹 Core Files
app.py
Initializes Flask app
Connects MySQL
Registers all routes (auth, trains, bookings, admin)
config.py
Stores DB credentials and secret key
requirements.txt
Contains dependencies (Flask, MySQL, Werkzeug)
🔹 Database
schema.sql
Creates all tables (users, trains, bookings)
Adds foreign key relations
Inserts default admin user
🔹 Backend (Routes)
auth.py
User registration (hashed password)
Login & session management
Role-based redirect (admin/user)
trains.py
Search trains by source & destination
Filters only active trains with available seats
bookings.py
Book tickets → generates PNR
Cancel booking → updates seat count
View booking history
Check PNR status
admin.py
Admin dashboard (stats)
Add trains
Activate/Deactivate trains
View all bookings
🔹 Frontend (Templates)
base.html
Common layout (navbar, alerts)
Dynamic navigation (user/admin)
index.html
Landing page with features & navigation
login.html & register.html
User authentication forms
search.html
Search trains
Displays available trains
book.html
Enter passenger details
Confirm booking
history.html
Shows user bookings
Cancel option available
pnr.html
Check booking status using PNR
🔹 Admin Templates
dashboard.html → Stats overview
trains.html → Manage trains
add_train.html → Add new trains
bookings.html → View all bookings
🎨 Styling
style.css
Modern UI design
Responsive layout
Cards, tables, forms styling
🔒 Security Notes
Passwords are hashed using Werkzeug
Sessions used for authentication
Avoid exposing DB credentials publicly
🚀 Future Enhancements
💳 Payment Integration
📧 Email Notifications
📱 Mobile Responsive UI
🎫 Seat Selection System
🤝 Contributing
