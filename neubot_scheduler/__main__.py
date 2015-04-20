#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Neubot scheduler process' main() """

from .frontend import Frontend

def main():
    """ Main function """
    frontend = Frontend()
    frontend.loop()

if __name__ == "__main__":
    main()
