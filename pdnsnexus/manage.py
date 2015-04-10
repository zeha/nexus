from flask.ext.script import Command, prompt_pass, Option
from pdnscontrol import app
from pdnscontrol.models import *
from flask.ext.security.utils import encrypt_password
from pdnsnexus.utils import fetch_json


class ResetPassword(Command):
    """Reset the password of any user"""

    option_list = (
        Option('email', help='E-Mail of the user to reset the password'),
    )

    def run(self, email):
        u = user_datastore.find_user(email=email)
        password = prompt_pass("New password for \"%s\"" % u.email)
        password2 = prompt_pass("New password (repeat)")
        if password != password2:
            print "Passwords do not match."
            return 1
        u.password = encrypt_password(password)
        db.session.add(u)
        db.session.commit()
        print "Password updated."
        return 0


class AddServer(Command):
    """Add a server to the server table"""

    option_list = (
        Option('server', help=''),
        Option('manager', help=''),
        Option('apikey', help=''),
    )

    def run(self, server, manager, api_key):
        url = server + '/servers/localhost'
        print "Contacting PowerDNS daemon at", url, "..."
        try:
            data = fetch_json(url, method='GET', headers={'X-API-Key': api_key})
        except Exception as except_inst:
            print "Fetching server information failed:", except_inst
            return 1

        url = manager + '/servers/localhost'
        print "Contacting pdnsmgrd at", url, "..."
        try:
            data = fetch_json(url, method='GET', headers={'X-API-Key': api_key})
        except Exception as except_inst:
            print "Fetching server information failed:", except_inst
            return 1

        server = Server()
        server.name = data['name']
        server.daemon_type = data['daemon_type']
        server.stats_url = server
        server.manager_url = manager
        server.api_key = api_key

        db.session.add(server)
        db.session.commit()
        print "Server", server.name, "added."
        return 0

