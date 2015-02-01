#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Blocking code """

from .mixins import HTTPRequestHandlerMixin
from .mixins import HTTPServerMixin
from .outqueue import HTTPOutputQueue
from .parser import HTTPParser

class _RequestHandler(HTTPRequestHandlerMixin):
    """ Replacement for SocketServer.BaseRequestHandler """

    def __init__(self, request, client_address, server, router):
        HTTPRequestHandlerMixin.__init__(self, router)
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        """ Called when the connection is ready """

    def handle(self):
        """ Called to handle the request """
        parser = HTTPParser()
        outqueue = HTTPOutputQueue()
        while True:
            data = self.request.recv(65535)
            if data:
                parser.feed(data)
            else:
                parser.eof()
            result = parser.parse()
            while result:
                outqueue.insert_data(self.emit(result))
                result = parser.parse()
            while outqueue:
                chunk = outqueue.get_next_chunk()
                if chunk:
                    self.request.sendall(chunk)
            if not data:
                break

    def finish(self):
        """ Called when we are done """

class HTTPRequestHandlerFactory(HTTPServerMixin):
    """ HTTP request handlers factory """

    def __call__(self, request, client_address, server):
        return _RequestHandler(request, client_address, server, self.router)
