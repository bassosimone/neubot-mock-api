#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot scheduler API """

import json
import logging
import os

from . import http
from . import utils

class StateManager(object):
    """ State manager """

    def __init__(self):
        self.comet_pending = []
        self.events = {
            "since": utils.timestamp(),
            "pid": os.getpid(),
        }
        self.current = "idle"
        self.tsnap = utils.opaque_time()

    def serialize(self):
        """ Serialize state manager """
        return http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps({
            "events": self.events,
            "current": self.current,
            "t": self.tsnap,
        }))

    def comet_wait(self, connection):
        """ Wait for Comet requests to be complete """
        self.comet_pending.append(connection)

    def comet_trigger(self):
        """ Trigger completion of Comet requests """
        comet_pending = self.comet_pending
        self.comet_pending = []
        for connection in comet_pending:
            try:
                connection.write(self.serialize())
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                logging.warning("unhandled exception", exc_info=1)

    def rootdir(self, connection):
        """ Generates the default HTML page """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "text/html",
        }, "<html></html>"))


STATE_MANAGER = StateManager()

def get():
    """ Get singleton instance """
    return STATE_MANAGER
