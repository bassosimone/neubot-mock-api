#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Runner """

from . import http

class Runner(object):
    """ Runner class """

    def run(self, connection, test, streaming):
        """ Trigger the runner """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

RUNNER = Runner()

def get():
    """ Get the default backend """
    return RUNNER
