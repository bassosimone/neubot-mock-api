#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Configuration DB """

import sqlite3

class ConfigDB(object):
    """
     Configuration DB class. The constructor receives the database
     path as first argument, and a dictionary describing configuration vars
     as second argument. The latter is something like this:

         {
             "enabled": {
                 "cast": int,
                 "default_value": 1,
                 "label": "Whether automatic tests are enabled"
             }
         }
    """

    def __init__(self, path, variables):
        self.conn = sqlite3.connect(path)
        self.variables = variables
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS config(
                             name TEXT PRIMARY KEY,
                             value TEXT);""")
        conf = self.select()
        for name in self.variables:
            if name not in conf:
                self.conn.execute("INSERT INTO config VALUES(?, ?);", (name,
                                  self.variables[name]["default_value"]))
        self.conn.commit()

    def select(self):
        """ Select configuration variables """
        result = {}
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, value FROM config;")
        for name, value in cursor:
            if name in self.variables:
                value = self.variables[name]["cast"](value)
                result[name] = value
        return result

    def select_labels(self):
        """ Select configuration labels """
        result = {}
        for name in self.variables:
            result[name] = self.variables[name]["label"]
        return result

    def update(self, dictionary):
        """ Internal function to set config """
        for name in dictionary.keys():
            if name not in self.variables:
                del dictionary[name]
        self.conn.executemany("INSERT OR REPLACE INTO config VALUES(?, ?);",
                              dictionary.items())
        self.conn.commit()
