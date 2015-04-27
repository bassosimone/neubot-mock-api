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
                             test TEXT,
                             report TEXT);""")

    def select(self, test, since, until, offset, limit):
        """ Select saved data """
        result = []
        cursor = self.conn.cursor()
        if test:
            cursor.execute("""SELECT * FROM data
                              WHERE timestamp >= ? AND
                                    timestamp < ? AND
                                    test = ?
                              LIMIT ? OFFSET ?;""", (
                           since, until, test, limit, offset))
        else:
            cursor.execute("""SELECT * FROM data
                              WHERE timestamp >= ? AND
                                    timestamp < ?
                              LIMIT ? OFFSET ?;""", (
                           since, until, limit, offset))

        for tpl in cursor:
            result.append({
                "timestamp": tpl[0],
                "test": tpl[1],
                "report": tpl[2],
            })
        return result

    def insert(self, timestamp, test, report, commit=True):
        """ Insert new result in database """
        self.conn.execute("""INSERT INTO data(timestamp, test,
                             report) VALUES(?, ?, ?);""",
                          (timestamp, test, report))
        if commit:
            self.conn.commit()

    def commit(self):
        """ Commit changes """
        self.conn.commit()
