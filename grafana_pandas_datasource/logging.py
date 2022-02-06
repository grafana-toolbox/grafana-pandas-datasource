import io
import logging
from logging.config import dictConfig
from pprint import pprint


def setup_logging(level=logging.INFO):
    log_format = "%(asctime)-15s.%(msecs)d [%(name)-25s] %(levelname)-7s: %(message)s"
    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": log_format,
                }
            },
            "handlers": {
                "wsgi": {
                    "class": "logging.StreamHandler",
                    "stream": "ext://flask.logging.wsgi_errors_stream",
                    "formatter": "default",
                }
            },
            "root": {"level": level, "handlers": ["wsgi"]},
        }
    )


class LoggingMiddleware(object):
    """
    - https://blog.caoyu.info/middleware-in-flask.html
    - https://gist.github.com/georgevreilly/5762777
    - https://stackoverflow.com/questions/67563385/how-do-i-access-response-content-in-wsgi-middleware-for-flask/67572634#67572634
    """

    def __init__(self, app):
        self._app = app

    def __call__(self, environ, start_response):

        errorlog = environ["wsgi.errors"]

        request_body_content, request_body_length = self.get_request_body(environ)
        pprint(("REQUEST", environ), stream=errorlog)
        pprint(("REQUEST-BODY", request_body_content), stream=errorlog)

        def log_response(status, headers, *args):
            pprint(("RESPONSE", status, headers), stream=errorlog)
            response = start_response(status, headers, *args)
            return response

        # Capture response body.
        app_iter = self._app(environ, log_response)
        body = b"".join(app_iter)
        pprint(("RESPONSE-BODY:", body))
        app_iter = [body]
        return app_iter

    def get_request_body(self, environ):
        """
        Get request body from WSGI environment.
        """
        content_length = environ.get("CONTENT_LENGTH")
        body = ""
        if content_length:
            if content_length == "-1":
                # This is a special case, where the content length is basically undetermined.
                body = environ["wsgi.input"].read(-1)
                content_length = len(body)
            else:
                content_length = int(content_length)
                body = environ["wsgi.input"].read(content_length)
            # Reset request body for the nested app.
            environ["wsgi.input"] = io.BytesIO(body)
        else:
            content_length = 0
        return body, content_length
