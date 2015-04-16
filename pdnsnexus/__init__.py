# (imagine ascii text art "nexus" here)

from flask import Flask, current_app
from flask.ext.security import Security, current_user
import os

from . import api
from .models import user_datastore


SERVICE_NAME = 'pdnsnexusd'



class Control(Flask):
    jinja_options = dict(Flask.jinja_options,
                         variable_start_string='{[',
                         variable_end_string=']}')

app = Control(__name__, instance_relative_config=True)


app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_URL_PREFIX'] = '/auth'
app.config['SECURITY_CHANGE_URL'] = '/change-password'
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_PASSWORD_HASH'] = 'pbkdf2_sha512'
app.config['SECURITY_PASSWORD_SALT'] = None
app.config['DEBUG'] = False
app.config['PREFERRED_URL_SCHEME'] = 'http'
app.config['IGNORE_SSL_ERRORS'] = False
app.config['REMOTE_TIMEOUT'] = 1.5
app.config['SERVER_WORKERS'] = 5
app.config['SERVER_MAX_REQUESTS'] = 1000
app.config['SERVER_BIND'] = '127.0.0.1:8086'


def verify_config():
    if not current_app.config['DATABASE_URI']:
        raise Exception('DATABASE_URI must be set in pdnsnexus.conf.')


app.verify_config = verify_config


@app.errorhandler(404)
def not_found(error):
    return 'Not found', 404


app.register_blueprint(api.mod, url_prefix='/api')

security = Security(app, user_datastore)
