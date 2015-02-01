#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" HTTP router """

import logging

from . import serializer

class HTTPRouter(object):
    """ API requests router """

    def __init__(self):
        self.default_route = None
        self.routes = {}

    def add_route(self, url, generator):
        """ Add a route to the router """
        self.routes[url] = generator

    def add_default_route(self, generator):
        """ Add the default route """
        self.default_route = generator

    def route(self, request):
        """ Route request """

        url = request["url"]
        logging.debug("http: router received url: %s", url)
        index = url.find("?")
        if index >= 0:
            url = url[:index]
            logging.debug("http: router url without query: %s", url)

        if url in self.routes:
            generator = self.routes[url](request)
        elif self.default_route:
            generator = self.default_route(request)
        else:
            generator = serializer.compose_error("404", "Not Found")

        logging.debug("http: router returning: %s", generator)

        return generator
