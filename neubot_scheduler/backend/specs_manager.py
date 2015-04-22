#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Tests manager """

from .. import http

class TestsManager(object):
    """ Tests manager class """

    def query_tests(self, connection, test):
        """ Query available tests """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

TESTS_MANAGER = TestsManager()

def get():
    """ Get the default tests manager """
    return TESTS_MANAGER
