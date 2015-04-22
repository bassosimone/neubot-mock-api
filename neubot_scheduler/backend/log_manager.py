#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Log manager """

from .. import http

class LogManager(object):
    """ Log manager class """

    def query_logs(self, connection, reverse, verbosity):
        """ Query available tests """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "[]"))

LOG_MANAGER = LogManager()

def get():
    """ Get the default log manager """
    return LOG_MANAGER
