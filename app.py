from flask import Flask
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)

    from routes.auth import auth
    from routes.trains import trains
    from routes.bookings import bookings
    from routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(trains)
    app.register_blueprint(bookings)
    app.register_blueprint(admin, url_prefix='/admin')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
