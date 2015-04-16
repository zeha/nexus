# -*- coding: utf-8 -*-
import gunicorn.app.base
import gunicorn.glogging
from gunicorn.config import Config
import os
import os.path
import platform
import argparse
import logging
import logging.handlers

install_path = os.path.abspath(os.path.dirname(__file__))
os.chdir(install_path)
import pdnsnexus


class NexusServerBackgroundLogger(gunicorn.glogging.Logger):
    def __init__(self, cfg):
        self.syslog_handler = None
        super(NexusServerBackgroundLogger, self).__init__(cfg)

    def setup(self, cfg):
        self.error_log.setLevel(logging.INFO)
        self.access_log.setLevel(logging.INFO)
        syslog_path = '/var/run/syslog' if platform.system() == 'Darwin' else '/dev/log'
        self.syslog_handler = logging.handlers.SysLogHandler(syslog_path)
        self.syslog_handler.setFormatter(logging.Formatter(self._get_fmt()))
        self.error_log.addHandler(self.syslog_handler)

    def _get_fmt(self):
        return ('pdnsnexusd[%d]:' % os.getpid()) + ' %(message)s'

    def close_on_exec(self):
        # reset pid in log format
        self.syslog_handler.setFormatter(logging.Formatter(self._get_fmt()))


class NexusServer(gunicorn.app.base.Application):

    def __init__(self, usage=None, prog=None):
        super(NexusServer, self).__init__(usage=usage, prog=prog)

    def load_config(self):
        self.cfg = Config(self.usage, prog=self.prog)
        self.cfg.set("default_proc_name", self.prog)
        self.cfg.set("proc_name", self.prog)
        self.cfg.set("preload_app", True)
        self.cfg.set("chdir", install_path)
        self.cfg.set("bind", pdnsnexus.app.config['SERVER_BIND'])
        self.cfg.set("workers", pdnsnexus.app.config['SERVER_WORKERS'])
        self.cfg.set("max_requests", pdnsnexus.app.config['SERVER_MAX_REQUESTS'])
        parser = argparse.ArgumentParser(prog=self.prog)
        parser.add_argument("--daemon", action='store_true',
                            help="background process")
        parser.add_argument("--pid", dest='pidfile', metavar='FILE', action='store',
                            help="If set, write PID to file FILE")
        args = parser.parse_args()
        self.cfg.set("daemon", args.daemon)
        if args.daemon:
            self.cfg.set("logger_class", NexusServerBackgroundLogger)
        self.cfg.set("pidfile", args.pidfile)

    def load(self):
        # bridge gunicorn and pdnsnexus logging together
        for handler in logging.getLogger("gunicorn.error").handlers:
            pdnsnexus.app.logger.addHandler(handler)
        pdnsnexus.app.logger.setLevel(logging.WARN)
        return pdnsnexus.app


def run():
    NexusServer(prog="pdnsnexusd").run()
