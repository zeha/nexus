#!/usr/bin/env python
from flask.ext.script import Manager
import pdnsnexus
import pdnsnexus.manage

mgr = Manager(pdnsnexus.app)
mgr.add_command("add-server", pdnsnexus.manage.AddServer())
mgr.add_command("reset-password", pdnsnexus.manage.ResetPassword())


def run():
    mgr.run()
