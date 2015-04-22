#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Configuration manager """

import json
import logging
import os
import uuid

from .. import http

BASEDIR = "./config/"

VALID_VARIABLES = {
    "enabled": int,
    "uuid": str,
}

LABELS = {
    "enabled": "Whether automatic tests are enabled",
    "uuid": "Unique identifier of this Neubot",
}

class ConfigManager(object):
    """ Configuration manager class """

    def __init__(self):
        conf = self.read_config()
        self._initialize(conf)
        self.write_config(conf)

    def _initialize(self, conf):
        """ Sanitize configuration """
        if "uuid" not in conf:
            conf["uuid"] = str(uuid.uuid4())
        if "enabled" not in conf:
            conf["enabled"] = 1

    @staticmethod
    def read_variable(name):
        """ Read single configuration variable """
        if name not in VALID_VARIABLES:
            return
        path = os.path.join(BASEDIR, name)
        if not os.path.isfile(path):
            return
        with open(path, "r") as filep:
            value = filep.read().strip()
            return VALID_VARIABLES[name](value)

    def read_config(self):
        """ Internal function to get config """
        conf = {}
        for name in os.listdir(BASEDIR):
            value = self.read_variable(name)
            if value is not None:
                conf[name] = value
        return conf

    def get_config(self, connection, wants_labels):
        """ Get settings """
        if wants_labels:
            obj_to_dump = LABELS
        else:
            obj_to_dump = self.read_config()
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(obj_to_dump)))

    @staticmethod
    def write_variable(name, value):
        """ Write single configuration variable """
        if name not in VALID_VARIABLES:
            return
        path = os.path.join(BASEDIR, name)
        with open(path, "w") as filep:
            filep.write(str(value) + "\n")

    def write_config(self, dictionary):
        """ Internal function to set config """
        for name, value in dictionary.items():
            self.write_variable(name, value)

    def set_config(self, connection, updated_settings):
        """ Change settings """
        self.write_config(updated_settings)
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, "{}"))

CONFIG_MANAGER = ConfigManager()

def get():
    """ Get the default configuration manager """
    return CONFIG_MANAGER
