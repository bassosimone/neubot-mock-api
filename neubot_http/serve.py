#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" HTTP main """

import asyncore
import logging
import socket
import sys

if sys.version_info[0] < 3:
    from SocketServer import TCPServer, ThreadingMixIn, ForkingMixIn
else:
    from socketserver import TCPServer, ThreadingMixIn, ForkingMixIn

from .blocking import HTTPRequestHandlerFactory
from .nonblocking import HTTPServerNonblocking

class _ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """ Threaded TCP server """
    allow_reuse_address = True
    daemon_threads = True

class _ForkedTCPServer(ForkingMixIn, TCPServer):
    """ Forked TCP server """
    allow_reuse_address = True

class _SingleTCPServer(TCPServer):
    """ Single TCP server """
    allow_reuse_address = True

def serve(settings):
    """ Starts HTTP server """

    settings.setdefault("backlog", 128)
    settings.setdefault("family", socket.AF_INET)
    settings.setdefault("hostname", "")
    settings.setdefault("mode", "async")
    settings.setdefault("port", 8080)
    settings.setdefault("rootdir", "")
    settings.setdefault("routes", {})
    settings.setdefault("www_handler", None)

    epnt = settings["hostname"], int(settings["port"])

    logging.debug("http: using %s core", settings["mode"])

    if settings["mode"] == "async":
        server = HTTPServerNonblocking()
        if settings["www_handler"]:
            server.override_www_handler(settings["www_handler"]())
        for key in settings["routes"]:
            server.add_route(key, settings["routes"][key])
        server.set_rootdir(settings["rootdir"])
        server.create_socket(settings["family"], socket.SOCK_STREAM)
        server.set_reuse_addr()
        server.bind(epnt)
        server.listen(settings["backlog"])
        asyncore.loop()

    else:
        factory = HTTPRequestHandlerFactory()
        if settings["www_handler"]:
            factory.override_www_handler(settings["www_handler"]())
        for key in settings["routes"]:
            factory.add_route(key, settings["routes"][key])
        factory.set_rootdir(settings["rootdir"])
        if settings["mode"] == "threaded":
            make_server = _ThreadedTCPServer
        elif settings["mode"] == "forked":
            make_server = _ForkedTCPServer
        elif settings["mode"] == "single":
            make_server = _SingleTCPServer
        else:
            raise RuntimeError("http: invalid core type")
        server = make_server(epnt, factory)
        server.serve_forever()
