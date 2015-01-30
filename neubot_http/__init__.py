#
# This file is part of Neubot <https://www.neubot.org/>.
#
# Neubot is free software. See AUTHORS and LICENSE for more
# information on the copying conditions.
#

"""
 Neubot HTTP library.

 Basic usage:

     import logging
     import neubot_http
     import socket

     def foobar(message):
         ''' Handles the /debug URL '''
         logging.debug("type: %s", message["type"])
         logging.debug("method: %s", message["method"])
         logging.debug("url: %s", message["url"])
         logging.debug("protocol: %s", message["protocol"])
         for key in message["headers"]:
             logging.debug("header: %s => %s", key, message["headers"][key])
         for chunk in message["body"]:
             logging.debug("chunk: %s", chunk)
         subgen = neubot_http.serializer.compose_response("200", "Ok", {
             "Content-Type": "application/json",
         }, "{}")
         for chunk in subgen:
             yield chunk

     # Commented out params are default values
     neubot_http.serve({
         #"backlog": 128,
         #"family": socket.AF_INET,
         "hostname": "127.0.0.1",    # default: ""
         #"mode": "async",           # otherwise: forked, threaded, single
         #"port": 8080,
         "rootdir": "/var/www",      # default: "" (= no rootdir)
         "routes": {                 # default: {}
             "/debug": foobar,
             "/debug/x": foobar
         }
     })
"""

from .serve import serve
from . import serializer
