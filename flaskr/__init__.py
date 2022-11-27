import os

from flask import Flask
from flask_mysqldb import MySQL

from .routes.route_events import route_events
from .routes.route_edit_events import route_edit_events
from .routes.route_join_events import route_join_events
from .routes.route_user_information import route_user_information
from .routes.route_user_authentication import route_user_authentication

def create_app(test_config = None):
    app = Flask(__name__)
    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "Nilak@2022"
    app.config["MYSQL_DB"] = "events"

    mysql = MySQL(app)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # routes
    route_events(app, mysql)
    route_edit_events(app, mysql)
    route_join_events(app, mysql)
    route_user_authentication(app, mysql)
    route_user_information(app, mysql)

    return app
