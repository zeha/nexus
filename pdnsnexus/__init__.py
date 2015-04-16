# (imagine ascii text art "nexus" here)

from flask import Flask, current_app
from flask.ext.security import Security, current_user
import os


class Control(Flask):
    jinja_options = dict(Flask.jinja_options,
                         variable_start_string='{[',
                         variable_end_string=']}')

app = Control(__name__, instance_relative_config=True)

app.config.from_object('pdnsnexus.default_settings')

# app.config.from_pyfile('pdnsnexus.conf')

app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_URL_PREFIX'] = '/auth'
app.config['SECURITY_CHANGE_URL'] = '/change-password'
app.config['SECURITY_SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = app.config['DATABASE_URI']


def verify_config():
    if not current_app.config['DATABASE_URI']:
        raise Exception('DATABASE_URI must be set in pdnsnexus.conf.')


app.verify_config = verify_config


@app.errorhandler(404)
def not_found(error):
    return 'Not found', 404


from . import api
app.register_blueprint(api.mod, url_prefix='/api')

from .models import user_datastore
security = Security(app, user_datastore)
