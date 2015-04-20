#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot scheduler process """

import os
import time

if os.name == "nt":
    __TICKS = time.clock
elif os.name == "posix":
    __TICKS = time.time
else:
    raise RuntimeError("Operating system not supported")

def ticks():
    """ Returns a real representing the most precise clock available
        on the current platform.  Note that, depending on the platform,
        the returned value MIGHT NOT be a timestamp.  So, you MUST
        use this clock to calculate the time elapsed between two events
        ONLY, and you must not use it with timestamp semantics. """
    return __TICKS()

