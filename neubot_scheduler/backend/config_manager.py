#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Configuration manager """

import json
import sqlite3
import uuid

from .. import http

DATABASE_FILE = "config.sqlite3"

CREATE_QUERY = """CREATE TABLE IF NOT EXISTS config(
    name TEXT PRIMARY KEY,
    value TEXT);"""

UPDATE_QUERY = "INSERT OR REPLACE INTO config VALUES( ?,?);"

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
        self.connection = sqlite3.connect(DATABASE_FILE)
        self.connection.row_factory = sqlite3.Row
        self.connection.execute(CREATE_QUERY)
        conf = self.read_config()
        for name in conf:
            if name not in VALID_VARIABLES:
                del conf[name]
        if "uuid" not in conf:
            conf["uuid"] = str(uuid.uuid4())
        if "enabled" not in conf:
            conf["enabled"] = 1
        self.write_config(conf)
        self.connection.commit()

    def read_config(self):
        """ Internal function to get config """
        conf = {}
        cursor = self.connection.cursor()
        cursor.execute("SELECT name, value FROM config;")
        for name, value in cursor:
            if name not in VALID_VARIABLES:
                continue
            conf[name] = VALID_VARIABLES[name](value)
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

    def write_config(self, dictionary):
        """ Internal function to set config """
        self.connection.executemany(UPDATE_QUERY, dictionary.items())
        self.connection.commit()

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
