"""
Copyright 2017 Linar <linar@jether-energy.com>
Copyright 2020-2022 Andreas Motl <andreas.motl@panodata.org>

License: GNU Affero General Public License, Version 3
"""
from flask import Flask
from flask_cors import CORS

from grafana_pandas_datasource import config
from grafana_pandas_datasource.logging import LoggingMiddleware, setup_logging


def create_app(test_config=None) -> Flask:
    """
    Create and configure the Flask application, with CORS.

    - https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
    - https://flask-cors.readthedocs.io/

    :param test_config:
    :return: Configured Flask application.
    """

    setup_logging()

    # Create Flask application.
    app = Flask(__name__)

    # Load configuration.
    app.config.from_object(config)

    # Initialize Cross Origin Resource sharing support for
    # the application on all routes, for all origins and methods.
    CORS(app)
    app.config["CORS_HEADERS"] = "Content-Type"

    # Optionally enable HTTP conversation tracing.
    if app.config.get("TRACE_CONVERSATION"):
        app.wsgi_app = LoggingMiddleware(app.wsgi_app)

    return app
