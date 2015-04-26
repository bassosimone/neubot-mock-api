#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" State tracker """

import logging
import os

from . import utils

class StateTracker(object):
    """ State tracker class """

    def __init__(self, opaque_time=None):
        if not opaque_time:
            opaque_time = utils.opaque_time
        self.opaque_time = opaque_time
        self.current = ""
        self.events = {
            "since": utils.timestamp(),
            "pid": os.getpid(),
        }
        self.tsnap = self.opaque_time()
        self.waiters = []

    def as_dict(self):
        """ Return current state as dict """
        return {
            "events": self.events,
            "current": self.current,
            "t": self.tsnap,
        }

    def subscribe(self, function, connection, request):
        """ Wait for state to change """
        self.waiters.append((function, connection, request))

    def update(self, current, event):
        """ Update state without publishing state change """
        self.current = current
        self.tsnap = self.opaque_time()
        self.events[current] = event

    def commit(self):
        """ Publish state change """
        waiters = self.waiters
        self.waiters = []
        for function, connection, request in waiters:
            try:
                function(connection, request)
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                logging.warning("unhandled exception", exc_info=1)
