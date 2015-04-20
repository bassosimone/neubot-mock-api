#!/usr/bin/env python

#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Example API implementation """

import asyncore
import json
import logging
import os
import sys

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))

from neubot_scheduler import http

def simple(connection, request):
    """ Handles / URL """
    response = {
        "method": request.method,
        "url": request.url,
        "protocol": request.protocol,
        "headers": request.headers,
        "body": request.body_as_string()
    }
    connection.write(http.writer.compose_response("200", "Ok", {
        "Content-Type": "application/json",
    }, json.dumps(response, indent=4)))

def main():
    """ Main function """
    logging.basicConfig(level=logging.DEBUG, format="%(message)s")
    http.listen({
        "routes": {
            "/": simple,
        }
    })
    asyncore.loop()

if __name__ == "__main__":
    main()
