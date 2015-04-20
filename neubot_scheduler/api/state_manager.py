#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot state manager """

from .. import http

class StateManager(object):
    """ State manager """

    def __init__(self):
        self.pending = []

    def serialize(self):
        """ Serialize state manager """
        return http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}")

    def comet_wait(self, connection):
        self.pending.append(connection)

    def comet_trigger(self):
        pending = self.pending
        self.pending = []
        for connection in pending:
            try:
                connection.write(self.serialize())
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                logging.warning("unhandled exception", exc_info=1)

STATE_MANAGER = StateManager()

def get():
    """ Get singleton instance """
    return STATE_MANAGER
