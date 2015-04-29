#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot scheduler process' main() """

import getopt
import logging
import sys

from .frontend import Frontend
from . import command_dump

def main():
    """ Main function """

    level = logging.WARNING
    mode = ""
    try:
        options, _ = getopt.getopt(sys.argv[1:], "v", ["dump"])
    except getopt.error:
        sys.exit("Usage: neubot-scheduler [-v] [--dump]")
    for name, _ in options:
        if name == "-v":
            level = logging.DEBUG
        elif name == "--dump":
            mode = "dump"

    logging.basicConfig(format="%(message)s", level=level)

    if mode == "dump":
        command_dump.dump(sys.stdout)
        sys.exit(0)

    frontend = Frontend()
    frontend.loop()

if __name__ == "__main__":
    main()
