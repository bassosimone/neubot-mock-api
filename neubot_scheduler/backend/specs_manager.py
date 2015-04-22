#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Tests manager """

import json
import os

from .. import http

BASEDIR = "./specs"

class TestsManager(object):
    """ Tests manager class """

    @staticmethod
    def read_spec(name):
        """ Read single spec """
        if name.startswith("."):
            return
        path = os.path.join(BASEDIR, name)
        if not os.path.isfile(path):
            return
        with open(path, "r") as filep:
            return json.load(filep)

    def query_specs(self, connection):
        """ Query available tests """
        specs = {}
        for name in os.listdir(BASEDIR):
            value = self.read_spec(name)
            if value is not None:
                specs[name] = value
        connection.write(http.writer.compose_response("200", "Ok", {
            "Content-Type": "application/json",
        }, json.dumps(specs)))

TESTS_MANAGER = TestsManager()

def get():
    """ Get the default tests manager """
    return TESTS_MANAGER
