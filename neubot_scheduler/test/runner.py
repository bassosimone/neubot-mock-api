#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Runner tests """

import unittest
import logging
import sys
import sched
import time

if __name__ == "__main__":
    sys.path.insert(0, ".")

from neubot_scheduler.runner import Runner

logging.basicConfig(level=logging.DEBUG, format="%(message)s")

class NormalUsageCase(unittest.TestCase):
    """ Normal usage case """

    def test_normal_usage(self):
        """ Tests normal usage """
        scheduler = sched.scheduler(time.time, time.sleep)

        Runner(scheduler.enter, "antani", [
            "/usr/bin/mtr", "--report-wide", "8.8.8.8"
        ], 30, None, None).run()

        scheduler.run()

if __name__ == "__main__":
    unittest.main()
