#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Log manager """

import sqlite3

class LogManager(object):
    """
     Log manager class. The constructor receives the database path as
     first argument.
    """

    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("""CREATE TABLE IF NOT EXISTS log(
                             timestamp NUMBER PRIMARY KEY,
                             tag TEXT,
                             severity TEXT,
                             entry TEXT);""")

    def select(self, since, until):
        """ Select saved log entries """
        result = []
        cursor = self.conn.cursor()
        cursor.execute("""SELECT timestamp, tag, severity, entry FROM log
                          WHERE timestamp >= ? AND
                                timestamp < ?;""", (
                       since, until))
        for timestamp, tag, severity, entry in cursor:
            result.append({
                "timestamp": timestamp,
                "tag": tag,
                "severity": severity,
                "entry": entry,
            })
        return result

    def insert(self, timestamp, tag, severity, entry, commit=False):
        """ Insert new log entry """
        self.conn.execute("""INSERT INTO log(timestamp, tag, severity,
                             entry) VALUES(?, ?, ?, ?);""",
                          (timestamp, tag, severity, entry))
        if commit:
            self.conn.commit()

    def commit(self):
        """ Commit changes """
        self.conn.commit()
