#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Data manager tests """

import json
import unittest
import sys
import uuid

if __name__ == "__main__":
    sys.path.insert(0, ".")

from neubot_scheduler.backend.data_manager import DataManager

class NormalUsageCase(unittest.TestCase):
    """ Normal usage case """

    def test_normal_usage(self):
        """ Tests normal usage """
        mgr = DataManager(":memory:")
        for timestamp in range(128):
            mgr.insert(timestamp, "x", json.dumps({"t": timestamp}, False))
        mgr.commit()
        sys.stdout.write("%s\n" % mgr.select("x", 0, 128, 7, 20))
        sys.stdout.write("%s\n" % mgr.select("x", 0, 128, 127, 20))
        sys.stdout.write("%s\n" % mgr.select("x", 0, 128, 128, 20))

if __name__ == "__main__":
    unittest.main()
