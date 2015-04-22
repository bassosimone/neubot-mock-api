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

def opaque_time():
    """ Returns the opaque time, i.e. the time used to identify
        events by the web user interface.  This is an integer, and
        is calculated as follows: ``int(10^6 * ticks())``.  So,
        the same caveat regarding ticks() also applies to this
        function. """
    return int(1000000 * ticks())

def timestamp():
    """ Returns an integer representing the number of seconds elapsed
        since the EPOCH in UTC. """
    return int(time.time())
