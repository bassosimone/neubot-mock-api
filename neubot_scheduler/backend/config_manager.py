#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Configuration manager """

from .. import http

class ConfigManager(object):
    """ Configuration manager class """

    def get_config(self, connection, wants_labels):
        """ Get settings """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

    def set_config(self, connection, updated_settings):
        """ Change settings """
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

CONFIG_MANAGER = ConfigManager()

def get():
    """ Get the default configuration manager """
    return CONFIG_MANAGER
