#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

""" Implements serve() function """

import asyncore
import logging
import socket
import sys

if sys.version_info[0] < 3:
    from SocketServer import TCPServer, ThreadingMixIn, ForkingMixIn
else:
    from socketserver import TCPServer, ThreadingMixIn, ForkingMixIn

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
    settings.setdefault("port", 8080)
    settings.setdefault("rootdir", "")
    settings.setdefault("routes", {})

    epnt = settings["hostname"], int(settings["port"])

    logging.debug("http: using %s core", settings["mode"])

    server = HTTPServerNonblocking()
    for key in settings["routes"]:
        server.add_route(key, settings["routes"][key])
    server.set_rootdir(settings["rootdir"])
    server.create_socket(settings["family"], socket.SOCK_STREAM)
    server.set_reuse_addr()
    server.bind(epnt)
    server.listen(settings["backlog"])
    asyncore.loop()
