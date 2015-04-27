#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Frontend of Neubot scheduler """

import asyncore
import logging
import sched
import time
import uuid

from .backend.config_db import ConfigDB
from .backend.data_db import DataDB
from .backend.logs_db import LogsDB
from .backend.net_tests_db import NetTestsDB

from .router import Router
from .state_tracker import StateTracker

from . import utils
from . import http

class Frontend(object):
    """ Neubot frontend """

    def __init__(self, periodic=30.0):
        self.periodic = periodic
        self.scheduler = sched.scheduler(utils.ticks, self._poll)
        self.sched_periodic_task_()
        self.state_tracker = StateTracker()
        http.listen({
            "port": 9774,
            "routes": Router(
                ConfigDB("./var/lib/neubot/scheduler/config.sqlite3", {
                    "enabled": {
                        "cast": int,
                        "default_value": 1,
                        "label": "Whether automatic tests are enabled"
                    },
                    "uuid": {
                        "cast": str,
                        "default_value": str(uuid.uuid4()),
                        "label": "Random unique indentifier"
                    }
                }),
                DataDB("./var/lib/neubot/scheduler/data.sqlite3"),
                LogsDB("./var/lib/neubot/scheduler/log.sqlite3"),
                NetTestsDB("./etc/neubot/net_tests"),
                self.state_tracker,
                self.scheduler.enter
            )
        })

    def sched_periodic_task_(self):
        """ Schedule periodic task """
        self.scheduler.enter(self.periodic, 0, self._periodic_task, ())

    def run_periodic_task_(self):
        """ Run the periodic task """
        self.state_tracker.commit()

    def _periodic_task(self):
        """ Periodic maintenance task """
        self.sched_periodic_task_()
        try:
            self.run_periodic_task_()
        except (SystemExit, KeyboardInterrupt):
            raise
        except:
            logging.error("frontend: unhandled exception", exc_info=1)

    @staticmethod
    def _poll(timeout):
        """ Poll for I/O events """
        if asyncore.socket_map:
            asyncore.loop(timeout, True, count=1)
        else:
            time.sleep(timeout)

    def loop(self):
        """ Run async loop """
        while True:
            try:
                self.scheduler.run()
            except (SystemExit, KeyboardInterrupt):
                raise
            except:
                logging.error("frontend: unhandled exception", exc_info=1)
