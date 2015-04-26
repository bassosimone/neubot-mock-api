#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Data DB """

import json
import sqlite3

class DataDB(object):
    """
     Data DB class. The constructor receives the database
     path as its first argument.
    """

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS data(
                             timestamp NUMBER PRIMARY KEY,
                             test_name TEXT,
                             json_string TEXT);""")

    def select(self, test_name, since, until, offset, limit):
        """ Select saved data """
        result = []
        cursor = self.conn.cursor()
        cursor.execute("""SELECT json_string FROM data
                          WHERE timestamp >= ? AND
                                timestamp < ? AND
                                test_name = ?
                          LIMIT ? OFFSET ?;""", (
                       since, until, test_name, limit, offset))
        for result_tuple in cursor:
            result.append(json.loads(result_tuple[0]))
        return result

    def insert(self, timestamp, test_name, json_string, commit=True):
        """ Insert new result in database """
        self.conn.execute("""INSERT INTO data(timestamp, test_name,
                             json_string) VALUES(?, ?, ?);""",
                          (timestamp, test_name, json_string))
        if commit:
            self.conn.commit()

    def commit(self):
        """ Commit changes """
        self.conn.commit()
