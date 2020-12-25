"""
Copyright 2017 Linar <linar@jether-energy.com>
Copyright 2020 Andreas Motl <andreas.motl@panodata.org>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None) -> Flask:
    """
    Create and configure the Flask application, with CORS.

    - https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/
    - https://flask-cors.readthedocs.io/

    :param test_config:
    :return: Configured Flask application.
    """

    # Create Flask application.
    app = Flask(__name__)

    # Initialize Cross Origin Resource sharing support for
    # the application on all routes, for all origins and methods.
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    return app
