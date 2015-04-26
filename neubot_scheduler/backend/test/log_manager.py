#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Log manager tests """

import json
import unittest
import sys
import uuid

if __name__ == "__main__":
    sys.path.insert(0, ".")

from neubot_scheduler.backend.log_manager import LogManager

class NormalUsageCase(unittest.TestCase):
    """ Normal usage case """

    def test_normal_usage(self):
        """ Tests normal usage """
        mgr = LogManager(":memory:")
        for timestamp in range(128):
            mgr.insert(timestamp, "x", "DEBUG", "antani")
        mgr.commit()
        sys.stdout.write("%s\n" % mgr.select(7, 27))

if __name__ == "__main__":
    unittest.main()
