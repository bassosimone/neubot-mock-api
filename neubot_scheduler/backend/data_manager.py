#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Data manager """

from .. import http

class DataManager(object):
    """ Data manager class """

    def query_data(self, connection, test, since, until):
        """ Query saved data """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

DATA_MANAGER = DataManager()

def get():
    """ Get the default data manager """
    return DATA_MANAGER
