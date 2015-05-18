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

def main():
    """ Main function """

    level = logging.WARNING
    mode = ""
    try:
        options, arguments = getopt.getopt(sys.argv[1:], "v")
    except getopt.error:
        sys.exit("Usage: neubot-scheduler [-v] /path/to/web/interface")
    if len(arguments) != 1:
        sys.exit("Usage: neubot-scheduler [-v] /path/to/web/interface")
    for name, _ in options:
        if name == "-v":
            level = logging.DEBUG

    logging.basicConfig(format="%(message)s", level=level)

    frontend = Frontend(arguments[0])
    frontend.loop()

if __name__ == "__main__":
    main()
