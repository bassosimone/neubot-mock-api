#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" StateTracker tests """

import unittest
import sys
import uuid

if __name__ == "__main__":
    sys.path.insert(0, ".")

from neubot_scheduler.state_tracker import StateTracker

class NormalUsageCase(unittest.TestCase):
    """ Normal usage case """

    def test_normal_usage(self):
        """ Tests normal usage """

        def opaque_time_gen():
            """ Fake out opaque time """
            count = [0]

            def opaque_time():
                """ Internal counter """
                cur = count[0]
                count[0] += 1
                return cur

            return opaque_time

        state_tracker = StateTracker(opaque_time_gen())
        sys.stdout.write("%s\n" % state_tracker.as_dict())

        def print_state(connection, request):
            """ Print state of the Neubot scheduler """
            sys.stdout.write("%d-%d: %s\n" % (connection, request,
                             state_tracker.as_dict()))

        state_tracker.subscribe(print_state, 1, 1)
        state_tracker.subscribe(print_state, 2, 2)
        state_tracker.update("negotiate", {"user_name": "antani"})
        state_tracker.update("test", {"speed": "1 Mbit/s"})
        state_tracker.commit()

if __name__ == "__main__":
    unittest.main()
