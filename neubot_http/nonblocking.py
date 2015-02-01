#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Nonblocking code """

import asyncore
import logging

from .mixins import HTTPRequestHandlerMixin
from .mixins import HTTPServerMixin
from .outqueue import HTTPOutputQueue
from .parser import HTTPParser

class _RequestHandler(asyncore.dispatcher, HTTPRequestHandlerMixin):
    """ Nonblocking request handler """

    def __init__(self, router, sock=None, mapx=None):
        asyncore.dispatcher.__init__(self, sock, mapx)
        HTTPRequestHandlerMixin.__init__(self, router)
        self.parser = HTTPParser()
        self.queue = HTTPOutputQueue()

    def handle_read(self):
        data = self.recv(65535)
        logging.debug("http: async recv %d", len(data))
        if data:
            self.parser.feed(data)
        else:
            self.parser.eof()
        result = self.parser.parse()
        while result:
            self.queue.insert_data(self.emit(result))
            result = self.parser.parse()

    def writable(self):
        return bool(self.queue)

    def handle_write(self):
        chunk = self.queue.get_next_chunk()
        if chunk:
            chunk = chunk[self.send(chunk):]
            if chunk:
                self.reinsert_partial_chunk(chunk)

class HTTPServerNonblocking(asyncore.dispatcher, HTTPServerMixin):
    """ Nonblocking HTTP server """

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        HTTPServerMixin.__init__(self)

    def handle_accept(self):
        result = self.accept()
        if not result:
            return
        sock = result[0]
        _RequestHandler(self.router, sock)
