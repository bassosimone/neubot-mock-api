#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Nonblocking code """

import asyncore
import collections
import logging

from .mixins import HTTPRequestHandlerMixin
from .mixins import HTTPServerMixin
from .parser import HTTPParser

class _RequestHandler(asyncore.dispatcher, HTTPRequestHandlerMixin):
    """ Nonblocking request handler """

    def __init__(self, router, sock=None, mapx=None):
        asyncore.dispatcher.__init__(self, sock, mapx)
        HTTPRequestHandlerMixin.__init__(self, router)
        self.parser = HTTPParser()
        self.obuff = collections.deque()

    def handle_read(self):
        data = self.recv(65535)
        logging.debug("http: async recv %d", len(data))
        if data:
            self.parser.feed(data)
        else:
            self.parser.eof()
        while True:
            result = self.parser.parse()
            if not result:
                break
            to_send = self.emit(result)
            if to_send:
                self.obuff.append(to_send)

    def writable(self):
        return bool(self.obuff)

    def handle_write(self):
        while self.obuff:
            selected = self.obuff[0]
            if isinstance(selected, bytes):
                if selected:
                    break
                self.obuff.popleft()
                continue
            try:
                data = next(selected)
            except StopIteration:
                self.obuff.popleft()
            else:
                if data:
                    self.obuff.appendleft(data)
                    break
        if self.obuff:
            self.obuff[0] = data[self.send(self.obuff[0]):]

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
