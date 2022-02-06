import logging
from logging.config import dictConfig


def setup_logging(level=logging.INFO):
    log_format = '%(asctime)-15s.%(msecs)d [%(name)-25s] %(levelname)-7s: %(message)s'
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': log_format,
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': level,
            'handlers': ['wsgi']
        }
    })
