#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Network tests DB """

import json
import os

class NetTestsDB(object):
    """ Network tests DB class """

    def __init__(self, basedir):
        self.basedir = basedir

    def read_one(self, name):
        """ Read single test descriptor """
        if name.startswith("."):
            return
        path = os.path.join(self.basedir, name)
        if not os.path.isfile(path):
            return
        with open(path, "r") as filep:
            return json.load(filep)

    def read_all(self):
        """ Read all tests descriptors """
        result = {}
        for name in os.listdir(self.basedir):
            value = self.read_one(name)
            if value is not None:
                result[name] = value
        return result
