#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Mixins used throughout the code """

from .router import HTTPRouter
from .www_handler import WWWHandler

class HTTPServerMixin(object):
    """ Common behavior of HTTP servers """

    def __init__(self):
        self.router = HTTPRouter()
        self.www_handler = WWWHandler()
        self.router.add_default_route(self.www_handler)

    def override_www_handler(self, www_handler):
        """ Override the WWW handler """
        self.www_handler = www_handler

    def add_route(self, url, generator):
        """ Add route """
        self.router.add_route(url, generator)

    def set_rootdir(self, rootdir):
        """ Add default route """
        self.www_handler.set_rootdir(rootdir)

class HTTPRequestHandlerMixin(object):
    """ Common behavior of HTTP request handlers """

    def __init__(self, router):
        self.router = router

    def emit(self, event):
        """ Emit the specified event """
        if event[0] == "request":
            return self.on_request_begin(event[1])
        elif event[0] == "data":
            return self.on_request_data(event[1], event[2])
        elif event[0] == "end":
            return self.on_request_end(event[1])
        else:
            raise RuntimeError

    def on_request_begin(self, request):
        """ Override to filter requests by headers """

    def on_request_data(self, request, data):
        """ Override to ignore incoming body """
        request.add_body_chunk(data)

    def on_request_end(self, request):
        """ Override to process complete requests """
        return self.router.route(request)
