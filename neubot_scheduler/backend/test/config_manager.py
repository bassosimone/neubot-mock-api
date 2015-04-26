#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Configuration manager tests """

import unittest
import sys
import uuid

if __name__ == "__main__":
    sys.path.insert(0, ".")

from neubot_scheduler.backend.config_manager import ConfigManager

class NormalUsageCase(unittest.TestCase):
    """ Normal usage case """

    def test_normal_usage(self):
        """ Tests normal usage """
        mgr = ConfigManager(":memory:", {
            "enabled": {
                "cast": int,
                "default_value": 1,
                "label": "Whether automatic tests are enabled",
            },
            "uuid": {
                "cast": str,
                "default_value": str(uuid.uuid4()),
                "label": "Random unique identifier",
            }
        })
        sys.stdout.write("%s\n" % mgr.select(False))
        mgr.update({
            "enabled": 0
        })
        sys.stdout.write("%s\n" % mgr.select(False))

if __name__ == "__main__":
    unittest.main()
