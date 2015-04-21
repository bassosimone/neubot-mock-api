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

from . import api
from . import utils
from . import http

class Frontend(object):
    """ Neubot frontend """

    def __init__(self, periodic=30.0):
        self.periodic = periodic
        self.scheduler = sched.scheduler(utils.ticks, self._poll)
        self.sched_periodic_task_()
        http.listen({
            "port": 9774,
            "routes": {
                "/api": api.api_,
                "/api/": api.api_,
                "/api/config": api.api_config,
                "/api/data": api.api_data,
                "/api/debug": api.api_debug,
                "/api/exit": api.api_exit,
                "/api/index": api.api_index,
                "/api/log": api.api_log,
                "/api/results": api.api_results,
                "/api/runner": api.api_runner,
                "/api/state": api.api_state,
                "/api/version": api.api_version,
            }
        })

    def sched_periodic_task_(self):
        """ Schedule periodic task """
        self.scheduler.enter(self.periodic, 0, self._periodic_task, (self,))

    @staticmethod
    def run_periodic_task_():
        """ Run the periodic task """
        logging.debug("periodic: trigger comet...")
        api.state_manager().comet_trigger()

    @staticmethod
    def _periodic_task(obj):
        """ Periodic maintenance task """
        obj.sched_periodic_task_()
        try:
            obj.run_periodic_task_()
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
