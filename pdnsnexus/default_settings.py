# Default settings loaded on app startup.
# Please keep the defaults in sync with
#     instance/pdnscontrol.conf.example.

DATABASE_URI = ''

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = None

PREFERRED_URL_SCHEME = 'http'
IGNORE_SSL_ERRORS = False
REMOTE_TIMEOUT = 1.5

DEBUG = False

SERVER_BIND = '127.0.0.1:8086'
SERVER_WORKERS = 4
SERVER_MAX_REQUESTS = 1000
