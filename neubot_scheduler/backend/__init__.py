#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" The backend """

from .. import http

class Backend(object):
    """ Backend class """

    def get_config(self, connection, wants_labels):
        """ Get settings """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

    def query_data(self, connection, test, since, until):
        """ Query saved data """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

    def query_logs(self, connection, reverse, verbosity):
        """ Query available tests """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "[]"))

    def query_tests(self, connection, test):
        """ Query available tests """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

    def rootdir(self, connection):
        """ Generates the default HTML page """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "text/html",
        }, "<html></html>"))

    def set_config(self, connection, updated_settings):
        """ Change settings """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

BACKEND = Backend()

def get():
    """ Get the default backend """
    return BACKEND
